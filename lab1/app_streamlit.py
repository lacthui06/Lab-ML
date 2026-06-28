import streamlit as st
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
import re

# ----------------- CUSTOM UNPICKLER TRÁNH LỖI CLASS ĐỊNH NGHĨA Ở NOTEBOOK -----------------
class SimpleModel:
    pass

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'LogisticRegressionFromScratch':
            return SimpleModel
        return super().find_class(module, name)

st.set_page_config(page_title="Email Spam Classifier", layout="centered")
st.title("📧 Email Spam Classifier (Inference & Runtime Evaluation)")

# ----------------- TẢI MODEL VÀ TIỀN XỬ LÝ -----------------
@st.cache_resource
def load_assets():
    try:
        with open('data/ready_train/preprocess_pack.pkl', 'rb') as f:
            prep = pickle.load(f)
        with open('modeling/logistic_model.pkl', 'rb') as f:
            model = CustomUnpickler(f).load()
        return prep, model
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy file mô hình hoặc bộ tiền xử lý. Hãy chạy streamlit từ thư mục chứa data và modeling.")
        return None, None

prep, loaded_model = load_assets()

if prep is not None and loaded_model is not None:
    # Phân tách model và threshold từ dict (hỗ trợ cả kiểu lưu cũ và kiểu lưu mới chứa threshold)
    if isinstance(loaded_model, dict):
        model = loaded_model['model']
        threshold = loaded_model.get('threshold', 0.5)
    else:
        model = loaded_model
        threshold = 0.5
else:
    model = None
    prep = None
    threshold = 0.5


def clean_email_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_domain_frequency(domain, freq_dict):
    domain_clean = str(domain).strip().lower()
    domain_with_bracket = domain_clean if domain_clean.endswith('>') else domain_clean + '>'
    domain_no_bracket = domain_clean[:-1] if domain_clean.endswith('>') else domain_clean
    
    for key in [domain_clean, domain_with_bracket, domain_no_bracket]:
        if key in freq_dict:
            return float(freq_dict[key])
    return 1.0

# Chế độ dự báo
mode = st.radio("Chọn chế độ dự đoán:", ["Dự đoán 1 Email đơn lẻ", "Dự đoán theo lô & Đánh giá (Batch Predict)"])

if mode == "Dự đoán 1 Email đơn lẻ":
    st.subheader("Nhập thông tin Email cần kiểm tra")
    sender = st.text_input("Người gửi (Sender):", "attacker@bad-domain.com")
    receiver = st.text_input("Người nhận (Receiver):", "user@company.cc")
    subject = st.text_input("Tiêu đề (Subject):", "Urgent: Update your security account now!")
    body = st.text_area("Nội dung (Body):", "We detected a security virus in your system. Please click here to resolve the attack.")
    urls_count = st.number_input("Số lượng URL trong thư:", min_value=0, value=1, step=1)
    

    if st.button("Dự đoán"):
        if prep and model:
            # 1. Trích xuất đặc trưng
            sender_domain = sender.split('@')[-1] if '@' in str(sender) else 'Unknown'
            receiver_domain = receiver.split('@')[-1] if '@' in str(receiver) else 'Unknown'
            sender_freq = get_domain_frequency(sender_domain, prep['sender_freq'])
            receiver_freq = get_domain_frequency(receiver_domain, prep['receiver_freq'])
            
            body_len_words = len(body.split())
            body_len_words_log = np.log1p(body_len_words)
            has_phishing = 1.0 if any(w in body.lower() for w in ['attack', 'crime', 'virus']) else 0.0
            is_reply = 1.0 if subject.lower().startswith('re:') else 0.0
            subject_len_words = float(len(subject.split()))
            
            stripped_sub = subject.strip()
            caps_ratio = sum(1 for c in stripped_sub if c.isupper()) / len(stripped_sub) if stripped_sub else 0.0
            
            meta_row = [body_len_words_log, float(urls_count), float(sender_freq), float(receiver_freq), has_phishing, is_reply, subject_len_words, caps_ratio]
            meta_cols = ['body_len_words_log', 'urls', 'sender_domain_freq', 'receiver_domain_freq', 'has_phishing', 'is_reply', 'subject_len_words', 'caps_ratio_subject']
            meta_df = pd.DataFrame([meta_row], columns=meta_cols)
            
            # 2. Tiền xử lý văn bản
            subject_clean = clean_email_text(subject)
            body_clean = clean_email_text(body)
            X_sub_tfidf = prep['tfidf_sub'].transform([subject_clean])
            X_msg_tfidf = prep['tfidf_msg'].transform([body_clean])
            X_meta_scaled = prep['scaler'].transform(meta_df)
            
            # 3. Kết hợp đặc trưng
            X_combined = hstack([X_sub_tfidf, X_msg_tfidf, csr_matrix(X_meta_scaled)])
            X_final = prep['selector'].transform(X_combined)
            
            # 4. Dự báo toán học chuẩn hóa (Sử dụng flatten thay vì .item để đồng bộ cấu trúc)
            z = np.asarray(X_final.dot(model.w)).flatten()[0] + model.b
            prob_spam = 1 / (1 + np.exp(-np.clip(z, -20, 20)))
            pred_label = 1 if prob_spam >= threshold else 0
            
            # 5. Hiển thị
            st.write("---")
            if pred_label == 1:
                st.error(f"Dự đoán: **SPAM** (Xác suất Spam: {prob_spam*100:.2f}%)")
            else:
                st.success(f"Dự đoán: **NOT SPAM** (Xác suất Spam: {prob_spam*100:.2f}%)")
                

else:
    st.subheader("Tải tập dữ liệu lô mới lên để đánh giá")
    uploaded_file = st.file_uploader("Tải file dữ liệu CSV hoặc JSON (phải chứa các cột sender, receiver, subject, body, urls_count và label):", type=["csv", "json"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_json(uploaded_file)
            
        st.write("Xem trước tập dữ liệu tải lên:")
        st.dataframe(df.head(5))
        
        if st.button("Chạy dự báo lô"):
            if prep and model:
                # --- PHÒNG VỆ CHỐNG DỮ LIỆU KHUYẾT (ANTI-CRASH) ---
                df['sender'] = df['sender'].fillna('').astype(str)
                df['receiver'] = df['receiver'].fillna('').astype(str)
                df['subject'] = df['subject'].fillna('').astype(str)
                df['body'] = df['body'].fillna('').astype(str)
                df['urls_count'] = df['urls_count'].fillna(0).astype(int)
                
                # --- TRÍCH XUẤT ĐẶC TRƯNG VECTOR HÓA (TỐC ĐỘ CAO) ---
                sender_domains = df['sender'].apply(lambda x: x.split('@')[-1] if '@' in x else 'Unknown')
                receiver_domains = df['receiver'].apply(lambda x: x.split('@')[-1] if '@' in x else 'Unknown')
                
                sender_freqs = sender_domains.apply(lambda d: get_domain_frequency(d, prep['sender_freq']))
                receiver_freqs = receiver_domains.apply(lambda d: get_domain_frequency(d, prep['receiver_freq']))
                
                body_lens = df['body'].apply(lambda x: len(x.split()))
                body_lens_log = np.log1p(body_lens)
                
                has_phishing = df['body'].str.lower().apply(lambda x: 1.0 if any(w in x for w in ['attack', 'crime', 'virus']) else 0.0)
                is_reply = df['subject'].str.lower().str.startswith('re:').astype(float)
                subject_lens = df['subject'].apply(lambda x: float(len(x.split())))
                
                caps_ratios = df['subject'].apply(lambda x: sum(1 for c in x.strip() if c.isupper()) / len(x.strip()) if x.strip() else 0.0)
                
                # Gom nhóm DataFrame Metadata
                meta_df = pd.DataFrame({
                    'body_len_words_log': body_lens_log,
                    'urls': df['urls_count'].astype(float),
                    'sender_domain_freq': sender_freqs,
                    'receiver_domain_freq': receiver_freqs,
                    'has_phishing': has_phishing,
                    'is_reply': is_reply,
                    'subject_len_words': subject_lens,
                    'caps_ratio_subject': caps_ratios
                })
                
                # --- PIPELINE BIẾN ĐỔI TOÀN BỘ BẢNG (KHÔNG DÙNG VÒNG LẶP) ---
                subjects_clean = df['subject'].apply(clean_email_text).tolist()
                bodies_clean = df['body'].apply(clean_email_text).tolist()
                
                X_sub_tfidf = prep['tfidf_sub'].transform(subjects_clean)
                X_msg_tfidf = prep['tfidf_msg'].transform(bodies_clean)
                X_meta_scaled = prep['scaler'].transform(meta_df)
                
                X_combined = hstack([X_sub_tfidf, X_msg_tfidf, csr_matrix(X_meta_scaled)])
                X_final = prep['selector'].transform(X_combined)
                
                # --- ĐẠO BÁO LOẠT BẰNG PHÉP NHÂN MA TRẬN KHÔNG GIAN THẤP ---
                z = np.asarray(X_final.dot(model.w)).flatten() + model.b
                prob_spam = 1 / (1 + np.exp(-np.clip(z, -20, 20)))
                y_pred = (prob_spam >= threshold).astype(int)
                
                # --- ĐÁNH GIÁ CHỈ SỐ ---
                st.write("---")
                if 'label' in df.columns:
                    y_true = df['label'].dropna().astype(int).to_numpy()
                    # Cắt bớt phần dự đoán tương ứng với nhãn khả dụng
                    y_pred = y_pred[:len(y_true)] 
                    
                    tp = np.sum((y_true == 1) & (y_pred == 1))
                    tn = np.sum((y_true == 0) & (y_pred == 0))
                    fp = np.sum((y_true == 0) & (y_pred == 1))
                    fn = np.sum((y_true == 1) & (y_pred == 0))
                    
                    acc = (tp + tn) / len(y_true) if len(y_true) > 0 else 0.0
                    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                    
                    st.success("Đã hoàn thành dự đoán lô dữ liệu mới!")
                    st.subheader("Chỉ số đánh giá thực tế của lô dữ liệu mới (Runtime Metrics):")
                    st.code(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f}")
                else:
                    st.warning("Tập dữ liệu tải lên không chứa cột 'label' để tính toán các chỉ số đánh giá.")
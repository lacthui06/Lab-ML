import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập giao diện trang web
st.set_page_config(
    page_title="Customer Segmentation App",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS để giao diện trông sang trọng hơn
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #6200ea;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #3700b3;
        color: white;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        font-weight: 500;
    }
    .vip-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important;
    }
    .spender-card {
        background: linear-gradient(135deg, #e91e63 0%, #9c27b0 100%);
    }
    .potential-card {
        background: linear-gradient(135deg, #00cbff 0%, #007adb 100%);
    }
    .frugal-card {
        background: linear-gradient(135deg, #00e676 0%, #00b0ff 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ Hệ Thống Phân Khúc Khách Hàng Trung Tâm Thương Mại")
st.markdown("Ứng dụng phân khúc khách hàng thời gian thực sử dụng thuật toán **K-Means Clustering**.")

# Xác định thư mục gốc của script app.py hiện tại
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tải các tệp tin deploy (scaler và centroids)
@st.cache_resource
def load_assets():
    # Load Scaler từ thư mục modeling
    scaler_path = os.path.join(BASE_DIR, 'modeling', 'scaler.pkl')
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    # Load Centroids từ thư mục modeling
    centroids_path = os.path.join(BASE_DIR, 'modeling', 'kmeans_centroids.npy')
    centroids = np.load(centroids_path)
    # Load dataset tiền xử lý để vẽ biểu đồ nền
    df_path = os.path.join(BASE_DIR, 'data', 'ready_train', 'shopping_mall_preprocessed.csv')
    df_clean = pd.read_csv(df_path)
    return scaler, centroids, df_clean

try:
    scaler, centroids, df_clean = load_assets()
except Exception as e:
    st.error(f"Lỗi tải tài nguyên deploy: {e}. Vui lòng đảm bảo các file 'scaler.pkl', 'kmeans_centroids.npy' và dữ liệu tiền xử lý ở đúng vị trí.")
    st.stop()

# Bố cục 2 cột chính
col_inputs, col_results = st.columns([1, 2])

with col_inputs:
    st.subheader("📝 Nhập Thông Tin Khách Hàng")
    
    annual_income = st.number_input("Thu nhập hàng năm ($)", min_value=20000, max_value=200000, value=80000, step=5000)
    spending_score = st.slider("Điểm chi tiêu (1 - 100)", min_value=1, max_value=100, value=50, step=1)
    
    st.write("---")
    predict_btn = st.button("Phân Loại Khách Hàng")

with col_results:
    if predict_btn:
        # 1. Chuẩn hóa dữ liệu đầu vào sử dụng scaler 3D (truyền dummy age=30 để thỏa mãn scaler 3 chiều)
        raw_input = np.array([[30, annual_income, spending_score]])
        scaled_input = scaler.transform(raw_input)
        income_scaled = scaled_input[0, 1]
        spending_scaled = scaled_input[0, 2]
        
        # Tạo vector đặc trưng 2D tương ứng với không gian huấn luyện (Income và Spend)
        user_features = np.array([[income_scaled, spending_scaled]])
        
        # 2. Tính khoảng cách Euclidean đến các tâm cụm 2D
        distances = np.linalg.norm(user_features - centroids, axis=1)
        predicted_cluster = np.argmin(distances)
        
        # 3. Định nghĩa thông tin phân khúc khách hàng 2D hành vi tài chính
        segments = {
            0: {
                "name": "Khách hàng VIP (High Income - High Spending)",
                "class_css": "vip-card", # Cam
                "desc": "Đây là nhóm khách hàng cốt lõi mang lại doanh thu cao nhất. Họ có thu nhập cao và thói quen chi tiêu phóng khoáng.",
                "action": "Tập trung các chiến dịch chăm sóc khách hàng VIP, gửi lời mời trải nghiệm sản phẩm cao cấp, cung cấp dịch vụ đặc quyền và quà tặng tri ân cá nhân hóa."
            },
            1: {
                "name": "Khách hàng Tiết Kiệm (Low Income - Low Spending)",
                "class_css": "spender-card", # Hồng/Đỏ
                "desc": "Nhóm khách hàng có thu nhập thấp và thói quen chi tiêu rất cẩn trọng, chỉ mua sắm khi thực sự cần thiết.",
                "action": "Tập trung giới thiệu các sản phẩm thuộc phân khúc bình dân, tích điểm đổi quà qua App di động, combo giảm giá ăn uống/vui chơi."
            },
            2: {
                "name": "Khách hàng Chi Tiêu Phóng Khoáng (Low Income - High Spending)",
                "class_css": "frugal-card", # Xanh lá
                "desc": "Nhóm khách hàng có thu nhập không quá cao nhưng lại mua sắm rất nhiều, ưu tiên trải nghiệm mua sắm và bắt kịp xu hướng.",
                "action": "Áp dụng các chiến dịch Marketing qua mạng xã hội, giới thiệu các sản phẩm bắt trend nhanh, khuyến mãi Flash Sale và hỗ trợ thanh toán trả góp."
            },
            3: {
                "name": "Khách hàng Cẩn Trọng / Tích Lũy (High Income - Low Spending)",
                "class_css": "potential-card", # Xanh dương
                "desc": "Nhóm khách hàng có thu nhập tốt nhưng chi tiêu ít và rất cẩn trọng. Họ ưu tiên chất lượng sản phẩm và giá trị tích lũy.",
                "action": "Gửi thông tin về các chương trình khuyến mãi gia dụng thiết yếu, chính sách hoàn tiền (cashback) và giảm giá hội viên thân thiết."
            }
        }
        
        seg_info = segments[predicted_cluster]
        
        # Hiển thị thẻ kết quả phân cụm đẹp mắt
        st.subheader("🎯 Kết Quả Phân Cụm")
        st.markdown(f"""
            <div class="card {seg_info['class_css']}">
                <h3>{seg_info['name']}</h3>
                <p><strong>Mô tả:</strong> {seg_info['desc']}</p>
                <p><strong>Chiến lược tiếp cận:</strong> {seg_info['action']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 4. Vẽ biểu đồ tán xạ động hiển thị vị trí khách hàng mới
        st.subheader("📍 Vị Trí Khách Hàng Trên Bản Đồ Phân Cụm (Chiếu 2D)")
        
        # Load labels cho tập dữ liệu nền theo mô hình 2D
        X_clean_2d = df_clean[['Annual Income_scaled', 'Spending Score_scaled']].values
        dists_clean = np.linalg.norm(X_clean_2d[:, np.newaxis] - centroids, axis=2)
        clean_labels = np.argmin(dists_clean, axis=1)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Khôi phục dữ liệu nền về thang đo gốc để biểu đồ dễ đọc
        income_raw_bg = df_clean['Annual Income_scaled'] * df_clean['Annual Income_scaled'].std() + df_clean['Annual Income_scaled'].mean()
        spending_raw_bg = df_clean['Spending Score_scaled'] * df_clean['Spending Score_scaled'].std() + df_clean['Spending Score_scaled'].mean()
        
        # Vẽ các điểm nền
        # 0: VIP (Orange), 1: Young Frugal (Pink), 2: Spender (Green), 3: Old Frugal (Blue)
        scatter_colors = {0: '#ffa500', 1: '#e91e63', 2: '#00e676', 3: '#007adb'}
        for c in range(4):
            idx = (clean_labels == c)
            ax.scatter(
                df_clean.loc[idx, 'Annual Income_scaled'],
                df_clean.loc[idx, 'Spending Score_scaled'],
                c=scatter_colors[c],
                alpha=0.25,
                s=20,
                label=segments[c]['name'].split(' (')[0]
            )
            
        # Vẽ các tâm cụm (Sử dụng đúng chỉ số của mô hình 2D: 0 là Income_scaled, 1 là Spending_score_scaled)
        ax.scatter(centroids[:, 0], centroids[:, 1], s=200, c='black', marker='X', label='Tâm cụm')
        
        # Vẽ vị trí khách hàng mới nhập (Ngôi sao đỏ viền vàng phát sáng)
        ax.scatter(income_scaled, spending_scaled, s=400, c='red', marker='*', edgecolors='yellow', linewidths=2.5, label='Khách hàng mới', zorder=10)
        
        ax.set_title("Vị trí khách hàng mới (Ngôi sao Đỏ) trên bản đồ 2D", fontsize=12, fontweight='bold')
        ax.set_xlabel("Thu nhập hàng năm (Chuẩn hóa)")
        ax.set_ylabel("Điểm chi tiêu (Chuẩn hóa)")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        st.pyplot(fig)
        
    else:
        # Trạng thái chờ
        st.info("💡 Vui lòng điền thông tin khách hàng ở bảng bên trái và nhấn nút **Phân Loại Khách Hàng** để xem kết quả phân khúc.")

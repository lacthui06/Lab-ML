import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import datetime

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Dự báo doanh số sản phẩm (SVR Production)",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. Định nghĩa lớp SVMRegressor để giải nén pickle thành công
class SVMRegressor:
    def __init__(self, lr=0.05, lamda=0.001, n_iters=1000):
        self.lr = lr
        self.lamda = lamda
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        pass

    def predict(self, X):
        raw_preds = X @ self.w + self.b
        return np.clip(raw_preds, 1.0, 10.0)

# 2. Tải mô hình và siêu tham số đã lưu
@st.cache_resource
def load_assets():
    model_path = "modeling/best_svm_model.pkl"
    scaler_path = "modeling/scaler_c1.pkl"
    metadata_path = "modeling/metadata.pkl"
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
        
    return model, scaler, metadata

try:
    model, scaler, metadata = load_assets()
    assets_loaded = True
except Exception as e:
    st.error(f"Lỗi tải tài nguyên mô hình: {e}. Vui lòng chạy xuất metadata trước.")
    assets_loaded = False

if assets_loaded:
    st.title("🔮 Dự Báo Số Lượng Bán Sản Phẩm (SVR)")
    st.markdown("Ứng dụng sử dụng mô hình **SVR Scratch** tốt nhất (Kịch bản **Median c1**, $R^2 = 83.76%$) để dự báo số lượng bán ra của sản phẩm.")

    # Danh mục và Địa điểm thực tế từ dữ liệu
    categories = [
        'Patisserie', 
        'Milk Products', 
        'Butchers', 
        'Beverages', 
        'Food', 
        'Furniture', 
        'Electric household essentials', 
        'Computers and electric accessories'
    ]
    locations = ['In-store', 'Online']
    payment_methods = ['Cash', 'Credit Card', 'Digital Wallet']

    # Suffix tương ứng với từng Category để lọc Item động
    suffix_map = {
        'Patisserie': '_PAT',
        'Milk Products': '_MILK',
        'Butchers': '_BUT',
        'Beverages': '_BEV',
        'Food': '_FOOD',
        'Furniture': '_FUR',
        'Electric household essentials': '_EHE',
        'Computers and electric accessories': '_CEA'
    }

    # 3. Đưa các input ra ngoài st.form để Streamlit tự động Rerun cập nhật danh sách
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox("Danh mục (Category):", categories)
        
        # Lọc danh sách Item động theo Category được chọn
        all_items = sorted(list(metadata['item_target_enc'].keys()))
        suffix = suffix_map.get(category, '')
        filtered_items = [it for it in all_items if it.endswith(suffix)]
        
        # Thêm key động để cập nhật mới widget khi Category đổi
        item = st.selectbox("Sản phẩm (Item):", filtered_items, key=f"item_select_{category}")
        
        # TỰ ĐỘNG TRA CỨU ĐƠN GIÁ tương ứng với Item đã chọn
        item_price = 15.0
        for (cat, pr), it in metadata['item_map'].items():
            if it == item:
                item_price = pr
                break
        
        # Điền giá trị đơn giá tự động tra cứu được vào ô nhập Price
        price = st.number_input("Đơn giá (Price Per Unit):", value=float(item_price), min_value=0.0, step=1.0, key=f"price_input_{item}")
        spent = st.number_input("Tổng tiền chi tiêu (Total Spent):", value=45.0, min_value=0.0, step=1.0)
        
    with col2:
        date = st.date_input("Ngày giao dịch (Transaction Date):", value=datetime.date.today())
        pay_method = st.selectbox("Phương thức thanh toán:", payment_methods)
        location = st.selectbox("Địa điểm mua hàng (Location):", locations)
        discount = st.checkbox("Áp dụng khuyến mãi (Discount Applied)", value=False)
        
    st.markdown("---")
    predict_btn = st.button("Dự báo Số lượng", use_container_width=True)

    # 4. Thực hiện Tiền xử lý & Dự báo khi bấm nút
    if predict_btn:
        # Khởi tạo các đặc trưng đầu vào
        input_features = {col: 0.0 for col in metadata['feature_cols']}
        g_vals = metadata['global_values']
        
        # Mặc định điền khuyết bằng trung vị (Median) của khách hàng từ tập huấn luyện
        input_features['Customer_Txn_Count'] = g_vals['global_txn_count']
        input_features['Customer_Avg_Quantity'] = g_vals['global_avg_qty']
        input_features['Customer_Avg_Spent'] = g_vals['global_avg_spent']

        # Target Encoding
        input_features['Item_Target_Enc'] = metadata['item_target_enc'].get(item, g_vals['global_qty_val'])
        input_features['Category_Target_Enc'] = metadata['cat_target_enc'].get(category, g_vals['global_qty_val'])

        # Đặc trưng thời gian
        dt = pd.to_datetime(date)
        input_features['Txn_Year'] = dt.year
        input_features['Txn_Month'] = dt.month
        input_features['Txn_Day'] = dt.day
        input_features['Txn_DayOfWeek'] = dt.dayofweek
        input_features['Txn_IsWeekend'] = 1 if dt.dayofweek >= 5 else 0

        # Đơn giá & Tổng tiền
        input_features['Price Per Unit'] = price
        input_features['Total Spent'] = spent
        
        # Áp dụng khuyến mãi
        input_features['Discount Applied'] = 1 if discount else 0

        # One-hot encoding tương thích với drop_first=True
        if pay_method == 'Credit Card':
            input_features['Payment Method_Credit Card'] = 1.0
        elif pay_method == 'Digital Wallet':
            input_features['Payment Method_Digital Wallet'] = 1.0
            
        if location == 'Online':
            input_features['Location_Online'] = 1.0

        # Chuẩn hóa
        num_df = pd.DataFrame([[input_features[col] for col in metadata['num_cols_c1']]], columns=metadata['num_cols_c1'])
        num_df_scaled = scaler.transform(num_df)
        for col, val in zip(metadata['num_cols_c1'], num_df_scaled[0]):
            input_features[col] = val

        # Tạo vector đầu vào và dự báo
        X_input = np.array([[input_features[col] for col in metadata['feature_cols']]])
        y_pred = model.predict(X_input)[0]

        # Hiển thị kết quả tinh gọn
        st.success(f"Số lượng bán dự báo (Quantity): **{y_pred:.2f}** sản phẩm")

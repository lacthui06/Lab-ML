# Hướng Dẫn Kỹ Thuật Ứng Dụng Streamlit (app.py) - Lab 2

Tài liệu này giải thích chi tiết cấu trúc, cơ chế hoạt động và cách thức xử lý dữ liệu của file ứng dụng [app.py](file:///C:/Users/Win%2011/Documents/ML/ML_proj_26/lab2/app.py) trong thư mục `lab2`.

---

## 1. Kiến Trúc Tổng Quan
Ứng dụng được xây dựng trên thư viện **Streamlit** chạy trực tiếp trên Python. Hệ thống hoạt động theo mô hình **Zero-Backend (Client-side execution)**:
*   Mô hình SVR đã huấn luyện (`best_svm_model.pkl`) và bộ chuẩn hóa (`scaler_c1.pkl`) được nạp trực tiếp vào bộ nhớ của ứng dụng Streamlit.
*   Khi người dùng tương tác, ứng dụng tự chạy ngầm quy trình xử lý dữ liệu đầu vào và gọi mô hình dự báo trực tiếp trên máy local, giúp tối ưu hóa hiệu năng và độ trễ bằng 0.

---

## 2. Giải Thích Các Bước Xử Lý Kỹ Thuật

### Bước 2.1: Đồng bộ hóa cấu trúc mô hình (`SVMRegressor`)
Do mô hình SVR được viết dưới dạng một lớp tùy biến từ đầu (SVR Scratch), thư viện `pickle` yêu cầu phải có khai báo của lớp `SVMRegressor` trong phạm vi scope của file nạp.
*   Chúng ta khai báo lại lớp `SVMRegressor` có hàm `predict()` thực hiện nhân ma trận $y = X \cdot w + b$ và giới hạn (clip) kết quả từ `1.0` đến `10.0` để khớp chính xác với hàm huấn luyện gốc.

### Bước 2.2: Tải Tài nguyên đã Lưu
*   Sử dụng trình trang trí `@st.cache_resource` để nạp các tệp pickle (`best_svm_model.pkl`, `scaler_c1.pkl`, `metadata.pkl`).
*   Việc sử dụng bộ nhớ đệm (cache) giúp ứng dụng chỉ phải đọc file từ ổ đĩa 1 lần duy nhất lúc khởi động, các lượt dự báo sau đó sẽ diễn ra ngay lập tức.

### Bước 2.3: Lọc sản phẩm động (Dynamic Item Filtering)
*   Trong dữ liệu gốc, mỗi mặt hàng có mã kết thúc bằng một hậu tố đại diện cho danh mục của nó (ví dụ: `_PAT` cho `Patisserie`, `_MILK` cho `Milk Products`).
*   Chúng ta tạo một từ điển ánh xạ `suffix_map`. Khi người dùng chọn danh mục `category`, ứng dụng sẽ lọc danh sách sản phẩm:
    ```python
    filtered_items = [it for it in all_items if it.endswith(suffix)]
    ```
*   Hộp chọn sản phẩm được gán khóa động `key=f"item_select_{category}"` để bắt buộc Streamlit tái tạo lại widget, tránh lỗi đệm widget của Streamlit khi dữ liệu danh sách thay đổi.

### Bước 2.4: Tự động nhảy đơn giá (Auto Price Lookup)
*   Để đơn giản hóa trải nghiệm người dùng, khi chọn một mã sản phẩm `Item`, ứng dụng sẽ tìm kiếm trong bản đồ liên kết `metadata['item_map']` để lấy mức đơn giá gốc tương ứng:
    ```python
    for (cat, pr), it in metadata['item_map'].items():
        if it == item:
            item_price = pr
    ```
*   Giá trị `item_price` tìm được sẽ được truyền làm mặc định cho ô số nhập liệu `price`.

### Bước 2.5: Tiền xử lý dữ liệu đầu vào (Inference Preprocessing Pipeline)
Khi người dùng nhấn nút **"Dự báo Số lượng"**, ứng dụng sẽ tái tạo lại đúng các bước đặc trưng đã thực hiện trên tập huấn luyện:
1.  **Thông số khách hàng (Customer ID):** Vì giao diện đã lược bỏ Customer ID, hệ thống tự động điền các đặc trưng tích lũy khách hàng bằng giá trị **Trung vị (Median)** toàn cục lấy từ tập Train.
2.  **Mã hóa Target Encoding:** Tra cứu giá trị mã hóa trung bình lượng bán của `Item` và `Category` được chọn.
3.  **Tách ngày giao dịch:** Tách `Transaction Date` thành Năm, Tháng, Ngày, Thứ trong tuần và Cuối tuần (0/1).
4.  **Mã hóa One-hot:** Chuyển đổi phương thức thanh toán và địa điểm đã chọn thành dạng nhị phân 0/1 tương thích với phương pháp `drop_first=True` khi huấn luyện mô hình.
5.  **Chuẩn hóa dữ liệu (StandardScaler):** Sử dụng bộ `scaler` đã fit trên tập Train để chuẩn hóa 12 đặc trưng số.
6.  **Dự báo (Predict):** Chuyển đổi dữ liệu thành vector 2D numpy array có hình dạng `(1, 16)` (khớp với 16 đặc trưng mô hình SVR nhận) và gọi hàm dự báo của mô hình SVR.

---

## 3. Tại sao không dùng `st.form`?
Trong Streamlit, các widget nằm bên trong cấu trúc `st.form` sẽ không bao giờ kích hoạt cơ chế Rerun (chạy lại file) khi người dùng thay đổi giá trị của chúng, cho đến khi bấm nút Submit.
*   Nếu dùng `st.form`, khi người dùng đổi danh mục, danh sách sản phẩm sẽ **không** được lọc lại động, và khi chọn sản phẩm mới, ô đơn giá đơn giá cũng sẽ **không** tự động cập nhật.
*   Do đó, việc đưa các input ra ngoài `st.form` và dùng nút bấm thường `st.button` là giải pháp bắt buộc để đạt được trải nghiệm tương tác động mượt mà.

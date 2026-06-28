# Tổng Quan Quy Trình Machine Learning - Lab 3 Customer Segmentation

Tài liệu này tóm tắt toàn bộ quy trình từ định nghĩa bài toán, lựa chọn dữ liệu, khảo sát mô hình và đưa ra quyết định lựa chọn mô hình cuối cùng phục vụ triển khai.

---

## 1. Định Nghĩa Bài Toán (Define Problem)
*   **Dạng bài toán**: Học không giám sát (Unsupervised Learning) - Gom cụm dữ liệu (Clustering).
*   **Mục tiêu**: Phân chia tệp 15,000 khách hàng của trung tâm thương mại thành các phân khúc (segments) riêng biệt có sự tương đồng cao về hành vi tài chính trong cùng một nhóm và sự khác biệt rõ rệt giữa các nhóm.
*   **Ứng dụng thực tế**: Giúp bộ phận Marketing thiết kế các chiến dịch cá nhân hóa (Personalized Marketing), tối ưu chi phí phân phát coupon và tăng tỷ lệ chuyển đổi mua sắm.

---

## 2. Lựa Chọn Dữ Liệu (Select Data)
Dữ liệu thô ban đầu gồm 5 cột: `Customer ID`, `Gender`, `Age`, `Annual Income`, và `Spending Score`. Quy trình chọn lọc đặc trưng cụ thể như sau:

*   **Loại bỏ các đặc trưng không phù hợp**:
    *   `Customer ID`: Bị loại bỏ đầu tiên vì đây là mã định danh tăng dần ngẫu nhiên, không mang thông tin hành vi và làm sai lệch khoảng cách Euclidean khi chạy mô hình.
*   **Khảo sát các tổ hợp dữ liệu (Feature Spaces)**:
    *   **Tổ hợp 2D (Core)**: `[Annual Income, Spending Score]` - Tập trung thuần túy vào hành vi tài chính chủ chốt (Khả năng chi trả vs Mức độ chi tiêu thực tế).
    *   **Tổ hợp 3D (Demographics)**: `[Age, Annual Income, Spending Score]` - Bổ sung thêm biến nhân khẩu học Tuổi tác.
    *   **Tổ hợp 3D (Ratio)**: `[Annual Income, Spending Score, Spending_to_Income_Ratio]` - Bổ sung thêm biến tương tác tự kỹ nghệ (Feature Engineering) để tính độ hoang phí tương đối.
    *   **Tổ hợp 4D/5D**: Đưa thêm biến `Gender` (đã mã hóa) để kiểm tra mức độ ảnh hưởng của giới tính.
*   **Kết luận lựa chọn dữ liệu đầu vào**:
    *   Quyết định chọn **Tổ hợp 2D (Annual Income & Spending Score)** làm đầu vào cho mô hình deploy cuối cùng vì đây là 2 đặc trưng có tính phân tách hình học cao nhất, trực tiếp biểu diễn hành vi mua sắm tại Mall mà không bị nhiễu bởi các biến nhân khẩu học phân bố đều như tuổi tác và giới tính.

---

## 3. Lựa Chọn Mô Hình (Select Model)
Chúng ta đã tiến hành thử nghiệm hai thuật toán gom cụm chính: **K-Means Clustering** và **DBSCAN**.

*   **Khảo sát DBSCAN**:
    *   *Đặc điểm*: Phân cụm dựa trên mật độ.
    *   *Kết quả*: Thất bại trên các không gian dữ liệu gốc (2D, 4D) vì phân bố dữ liệu giả lập của Mall quá đều (uniform grid), không có khoảng trống mật độ tự nhiên. DBSCAN chỉ hoạt động được khi thêm biến tương tác `Ratio` được tạo phi tuyến để kéo giãn hình học.
*   **Khảo sát K-Means (K-Means Scratch)**:
    *   *Đặc điểm*: Phân cụm dựa trên phân hoạch khoảng cách đến tâm cụm.
    *   *Kết quả*: Hoạt động ổn định trên mọi không gian đặc trưng. Thuật toán tự chia không gian dữ liệu thành các phân vùng hình học rất rõ nét.
*   **Quyết định chọn mô hình**:
    *   Chọn thuật toán **K-Means Scratch** cấu hình với tham số **$K=4$ cụm**, khởi tạo **`random`**, giới hạn tối đa **`max_iter=100`** chạy trên không gian **2D**.
    *   *Lý do lựa chọn*:
        1.  **Chỉ số Silhouette cao nhất (0.4117)** so với các không gian nhiều chiều hơn (3D: 0.3992; 5D: 0.2634).
        2.  **Giá trị thực tiễn cao**: Chia đều khách hàng thành 4 cụm tương ứng với 4 góc phần tư tài chính trực quan: **VIP** (Thu nhập cao - Chi tiêu cao), **Tiết kiệm** (Thu nhập thấp - Chi tiêu thấp), **Chi tiêu phóng khoáng** (Thu nhập thấp - Chi tiêu cao), và **Cẩn trọng** (Thu nhập cao - Chi tiêu thấp). Điều này giúp phòng Marketing dễ dàng định vị và triển khai chiến lược.

---

## 4. Quy Trình Thực Thi Chi Tiết (ML Flow)
Quy trình huấn luyện và chạy thử nghiệm được tự động hóa trong file notebook [modeling.ipynb](file:///C:/Users/Win%2011/Documents/ML/ML_proj_26/lab3/modeling/modeling.ipynb):

1.  **Data Preparation**: Load tập dữ liệu đã chuẩn hóa thang đo chuẩn (`StandardScaler`) từ bước feature engineering.
2.  **Model Definition**: Khởi tạo lớp `KMeansScratch` với công thức tính khoảng cách Euclidean tối ưu hóa ma trận.
3.  **Feature Space Exploration**: Huấn luyện thử nghiệm K-Means trên 5 không gian từ 2D đến 5D với $K \in [2, 9]$.
4.  **Elbow Optimization**: Đánh giá đồ thị Inertia (SSE) để xác nhận điểm cùi chỏ tối ưu bằng phương pháp Satopaa.
5.  **Hyperparameter Grid Search**: Chạy Grid Search quét qua các tổ hợp $K$, `max_iters`, và phương pháp khởi tạo (`random` vs `kmeans++`) để tìm ra thiết lập tối ưu nhất cho từng không gian đặc trưng.
6.  **Visualization & Save**: Vẽ biểu đồ so sánh chất lượng phân cụm và lưu tâm cụm tốt nhất của mô hình 2D (`kmeans_centroids.npy`) phục vụ deploy Web App Streamlit.

# Kế hoạch triển khai - Viết code huấn luyện mô hình từ đầu (From Scratch) cho Logistic Regression

Kế hoạch này thực hiện viết code huấn luyện mô hình **từ đầu (From Scratch)**, tìm kiếm siêu tham số (Hyperparameter Tuning), và đánh giá mô hình (Evaluation) cho thuật toán: Logistic Regression tích hợp vào file notebook trong thư mục `C:\Users\Win 11\Documents\ML\ML_proj_26\lab\lab1`.

## User Review Required

> [!IMPORTANT]
> - **Triển khai thuật toán từ đầu (From Scratch):** Class mô hình (`LogisticRegression`) sẽ được viết bằng code Python thuần và NumPy/SciPy, không sử dụng class phân loại `LogisticRegression` của thư viện `scikit-learn`. Thư viện `scikit-learn` chỉ được dùng để hỗ trợ chia tập dữ liệu, chuẩn hóa và tính toán các chỉ số đánh giá (như `classification_report`, `roc_curve`).
> - **Tối ưu hóa cho Ma trận thưa (Sparse Matrix):** Vì dữ liệu email sau bước TF-IDF có kích thước lớn ($31323 \times 3500$) và rất thưa, chúng tôi sẽ sử dụng các phép toán ma trận được tối ưu hóa bằng vector (Vectorized Operations) trên định dạng thưa của SciPy để tránh lỗi tràn bộ nhớ (Out-of-Memory) và tăng tốc độ huấn luyện/dự báo.

## Proposed Changes

### [Component: Jupyter Notebooks - Model Training & Evaluation]

We will modify/create the Logistic Regression notebook file in `C:\Users\Win 11\Documents\ML\ML_proj_26\lab\lab1\`.

---

#### [NEW] [logistic.ipynb](file:///C:/Users/Win%2011/Documents/ML/ML_proj_26/lab/lab1/logistic.ipynb)
Tạo mới notebook Hồi quy Logistic từ đầu bao gồm các phần:
1. **Tải dữ liệu:** Load các file đặc trưng `X_train_final.npz`, `X_test_final.npz`, `y_train.pkl`, `y_test.pkl`.
2. **Xây dựng Class Logistic Regression từ đầu:**
   - Tối ưu hóa gradient descent trực tiếp trên ma trận thưa sử dụng `.dot()` của SciPy.
   - Hàm sigmoid tránh lỗi tràn số bằng cách giới hạn biên (`np.clip`).
   - Ghi lại lịch sử hàm mất mát (Binary Cross-Entropy Loss) sau mỗi epoch để vẽ đồ thị hội tụ.
3. **Tìm kiếm siêu tham số:**
   - Thử nghiệm các tốc độ học theo thang logarit **`learning_rate` $\in \{0.001, 0.005, 0.01, 0.05, 0.1, 0.5\}$**, **`n_iters` $\in \{500, 1000, 1500, 2000\}$** để trực quan hóa rõ nét quá trình hội tụ.
   - *Lý do chọn khoảng này:* Thang logarit giúp bao quát từ tốc độ học nhỏ, an toàn nhưng hội tụ chậm ($0.001, 0.005$), đến mức vừa phải để cân bằng ($0.01, 0.05$), và các tốc độ học lớn ($0.1, 0.5$) để quan sát xem mô hình có bị hiện tượng dao động mạnh quanh cực trị (gradient bouncing) hoặc không thể hội tụ hay không.
4. **Vẽ biểu đồ hội tụ (Learning Curve):**
   - Trực quan hóa giá trị Loss giảm dần theo số epoch của các learning rate để so sánh tốc độ hội tụ.
5. **Huấn luyện & Đánh giá:**
   - Đo thời gian huấn luyện và dự báo (ms).
   - Xuất báo cáo phân loại chi tiết, vẽ ma trận nhầm lẫn và đường cong ROC-AUC.

---

## Verification Plan

### Automated Tests
- Tạo script Python độc lập `test_scratch_logistic.py` chạy thử thuật toán Logistic Regression tự viết trên tập dữ liệu đã lưu để đảm bảo không có lỗi cú pháp, tính toán sai lệch hay lỗi tràn bộ nhớ trước khi đưa vào notebook chính thức.

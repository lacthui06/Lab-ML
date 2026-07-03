# Kế hoạch & Thiết kế Triển khai Hồi quy SVR (Scratch) - Lab 2 Modeling

Tài liệu này ghi nhận kế hoạch thiết kế thuật toán, kế hoạch so sánh kịch bản và các điểm thảo luận kỹ thuật quan trọng cho phần Modeling.

---

## 1. Thiết kế Thuật toán SVR Scratch (Hồi quy Vector Hỗ trợ)
Chúng ta sẽ tự xây dựng lớp hồi quy SVR từ đầu sử dụng hàm tổn hao **$\epsilon$-insensitive loss** và cập nhật trọng số bằng **Gradient Descent** để tối ưu hóa khoảng cách dự báo đến nhãn thực tế.

### Cấu trúc lớp hồi quy SVR dự kiến:
```python
import numpy as np

class SVMRegressor:
    def __init__(self, lr=0.05, lamda=0.001, n_iters=1000):
        self.lr = lr
        self.lamda = lamda
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_sample, n_feature = X.shape
        self.w = np.zeros(n_feature)
        self.b = np.mean(y)

        for _ in range(self.n_iters):
            preds = X @ self.w + self.b
            errors = y - preds
            grad_coef = np.where(errors < 0, 1.0, np.where(errors > 0, -1.0, 0.0))
            grad_w = 2 * self.lamda * self.w + (1.0 / n_sample) * (X.T @ grad_coef)
            grad_b = (1.0 / n_sample) * np.sum(grad_coef)
            self.w -= self.lr * grad_w
            self.b -= self.lr * grad_b

    def predict(self, X):
        raw_preds = X @ self.w + self.b
        return np.clip(raw_preds, 1.0, 10.0)
```

---

## 2. Kế hoạch So sánh 6 Cấu hình (Mean vs Median Imputation)
Theo đúng định hướng thảo luận, chúng ta sẽ thực hiện so sánh hiệu năng của mô hình trên **6 cấu hình dữ liệu** để đánh giá ảnh hưởng của phương pháp điền khuyết (Imputation) và cấu trúc đặc trưng:

### 2.1. Thiết lập 2 nhánh điền khuyết (NaN Imputation):
*   **Nhánh 1 (Mean Imputation):** Điền khuyết các ô NaN của đơn giá/tổng chi tiêu và khách hàng mới bằng giá trị **Mean** (Trung bình).
*   **Nhánh 2 (Median Imputation):** Điền khuyết các ô NaN của đơn giá/tổng chi tiêu và khách hàng mới bằng giá trị **Median** (Trung vị).
*   *Lưu ý:* Các đặc trưng tích lũy (`Customer_Avg_Spent`) và Target Encoding vẫn tính toán bằng công thức Mean theo đúng bản chất toán học của chúng trên cả 2 nhánh.

### 2.2. So sánh 3 kịch bản đặc trưng (c1, c2, c3):
*   **Kịch bản c1 (Giữ cả Price và Spent):** Giữ nguyên hai biến đơn giá và tổng chi tiêu nhằm tận dụng mối quan hệ vật lý trực tiếp.
*   **Kịch bản c2 (Bỏ Total Spent):** Loại bỏ cột `Total Spent` để kiểm chứng xem mô hình có thể hoạt động chỉ dựa trên đơn giá và thông tin khách hàng hay không.
*   **Kịch bản c3 (Gộp bằng PCA):** Gộp hai biến `Price Per Unit` và `Total Spent` bằng thuật toán PCA tuyến tính để kiểm tra khả năng giảm chiều đặc trưng.

---

## 3. Quy trình Tuning & Đánh giá (Grid Search)
Chúng ta sẽ thực hiện Grid Search độc lập cho từng cấu hình trong số 6 kịch bản để tìm ra tham số tối ưu (`lr` từ `0.001` đến `0.05` và `lamda` từ `0.001` đến `0.1`), sau đó đo lường hiệu năng trên tập Test bằng các chỉ số: $R^2$, MSE, MAE, MAPE.

---

## 4. Thảo Luận Các Điểm Kỹ Thuật Quan Trọng

### 4.1. Ngưỡng chặn trên dự báo (Clipping Limit): 10.0 vs 16.0
*   **Ngưỡng 16.0:** Tính toán từ phân tích outlier của EDA chỉ ra cận trên thống kê là `15.5`. Khi thiết lập giới hạn là `16.0` trong predict, mô hình đạt độ chính xác $R^2 = 83.07\%$.
*   **Ngưỡng 10.0:** Đây là giới hạn vật lý thực tế của cột `Quantity` trong dữ liệu (không có hóa đơn nào mua quá 10 sản phẩm). Khi ép mô hình giới hạn ở mức tối đa vật lý này, ta loại bỏ được sai số dự đoán quá mức, giúp $R^2$ tăng lên mức tối ưu là **`83.76%`**.

### 4.2. Thảo luận kết quả của các kịch bản c1, c2, c3
*   **c1 (Giữ cả hai):** Hiệu năng vượt trội vì giữ được mối quan hệ chia tỷ lệ trực tiếp để tính Quantity.
*   **c2 (Bỏ Spent):** Thất bại hoàn toàn ($R^2 \approx -0.6\%$) do thiếu thông tin quy mô giao dịch.
*   **c3 (Gộp PCA):** Hiệu năng kém ($R^2 \approx 13.27\%$) do phép chiếu tuyến tính PCA làm triệt tiêu quan hệ chia phi tuyến giữa Price và Spent.
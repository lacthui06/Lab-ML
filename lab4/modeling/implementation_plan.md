# Kế hoạch cải tiến Modeling (Huấn luyện và Đánh giá trên Thang giá thực tế bằng hàm .score())

Kế hoạch này điều chỉnh toàn bộ quy trình huấn luyện và đánh giá mô hình theo yêu cầu mới từ bạn:
1. **Huấn luyện trên thang giá thực tế**: Loại bỏ biến đổi logarit cho biến mục tiêu `price`. Huấn luyện trực tiếp các mô hình để dự báo giá USD gốc (`price`).
2. **Sử dụng duy nhất 1 độ đo (R^2 Score)**: Chỉ đánh giá và so sánh các mô hình bằng chỉ số **$R^2$ Score** (hệ số xác định).
3. **Sử dụng hàm `.score()` của thư viện**: Sử dụng trực tiếp phương thức `model.score(X, y)` của Scikit-Learn để tính toán $R^2$ trên cả tập Train và tập Test. Loại bỏ hoàn toàn các chỉ số MAE, RMSE và MAPE.

---

## Chi tiết các thay đổi đề xuất

### 1. Phần Feature Engineering ([feature_engineer.ipynb](file:///C:/Users/Win%2011/Documents/AI/proj%20AI%20ML/feature%20egineer/feature_engineer.ipynb))
- **Bước 0**: Đọc dữ liệu, loại bỏ các dòng bị khuyết thiếu `price`.
- **Bước 2**: **Không áp dụng logarit** cho `price` nữa (chỉ áp dụng logarit cho diện tích `area_sqft_log` để nén các giá trị diện tích cực đại và capping phòng ngủ).
- **Bước 7**: Lưu tập Train/Test đã làm sạch ra thư mục [data/ready_train](file:///C:/Users/Win%2011/Documents/AI/proj%20AI%20ML/data/ready_train) dưới dạng các file `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` (trong đó `y_train` và `y_test` chỉ chứa cột `price` gốc thang USD).

### 2. Phần Modeling ([modeling.ipynb](file:///C:/Users/Win%2011/Documents/AI/proj%20AI%20ML/modeling/modeling.ipynb))
- **Bước 1**: Đọc dữ liệu từ thư mục `ready_train`.
- **Bước 2 & 3 (Xây dựng mô hình & Tìm siêu tham số)**:
  - Huấn luyện mô hình trực tiếp trên `y_train['price']`.
  - Sử dụng `GridSearchCV` với tham số `scoring='r2'` để tìm kiếm các tham số tối ưu:
    - **Linear Regression**: Tune `fit_intercept`.
    - **Random Forest Regressor**: Tune `n_estimators`, `max_depth`, `min_samples_split`.
    - **MLP Regressor**: Tune `hidden_layer_sizes`, `activation`, `alpha`.
- **Bước 4**: Vẽ biểu đồ hội tụ (Learning Curve) dựa trên điểm số $R^2$ (`scoring='r2'`) cho cả 3 mô hình.
- **Bước 5 (Đánh giá & Đối sánh)**:
  - Đo thời gian huấn luyện và thời gian dự báo (ms).
  - Tính toán điểm số $R^2$ trực tiếp bằng phương thức của thư viện:
    - `train_r2 = model.score(X_train, y_train['price'])`
    - `test_r2 = model.score(X_test, y_test['price'])`
  - Hiển thị bảng đối sánh 3 mô hình chứa các cột: `Mô hình`, `Thời gian Train (ms)`, `Thời gian Dự báo (ms)`, `Train R^2 Score`, `Test R^2 Score`.

---

## Kế hoạch kiểm thử & Xác minh
- Chạy thử liên hoàn cả 2 notebook `feature_engineer.ipynb` và `modeling.ipynb` để đảm bảo:
  - Tất cả các cell thực thi thành công không có lỗi.
  - Các kết quả đo lường được tính trực tiếp từ hàm `.score()` của Scikit-Learn trên thang đo thực tế USD và hiển thị đầy đủ bảng đối sánh.

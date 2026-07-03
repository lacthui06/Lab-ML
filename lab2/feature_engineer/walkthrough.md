# Hướng Dẫn Từng Bước Quy Trình Feature Engineering - Lab 2

Tài liệu này giải thích chi tiết ý nghĩa, phương pháp và lý do thực hiện của từng bước trong file notebook `feature_engineering.ipynb`.

---

## Bước 1. Chia Tách Dữ Liệu (Train/Test Split)
*   **Hành động:** Chia tập dữ liệu thô thành tập Huấn luyện (Train - 80%) và tập Kiểm thử (Test - 20%).
*   **Lý do thực hiện:** 
    *   Đây là bước bắt buộc đầu tiên trong mọi quy trình Học máy nhằm **ngăn chặn rò rỉ dữ liệu (Data Leakage)**.
    *   Mọi giá trị thống kê (Mean, Median, Mode, hoặc bản đồ liên kết) đều chỉ được phép tính toán trên tập Train và áp dụng (transform) sang tập Test. Nếu chúng ta xử lý trên toàn bộ tập dữ liệu trước khi chia, tập Train sẽ bị "học lỏm" thông tin từ tập Test, dẫn đến kết quả đánh giá mô hình bị ảo (quá lạc quan nhưng thực tế kém).

---

## Bước 2. Xử Lý Giá Trị Thiếu (Handling Missing Values)

### Bước 2.1: Phục hồi đơn giá (`Price Per Unit`) bằng công thức logic
*   **Hành động:** Sử dụng công thức vật lý `Price Per Unit = Total Spent / Quantity` để tính toán lại các ô bị trống của đơn giá đối với những dòng có đầy đủ tổng tiền và số lượng.
*   **Lý do thực hiện:** 
    *   Đây là phương pháp **phục hồi dữ liệu chính xác tuyệt đối (100%)** dựa trên mối quan hệ toán học hiển nhiên của dữ liệu kinh doanh.
    *   Phương pháp này luôn tốt hơn việc điền khuyết bằng thống kê (Mean/Median) vì nó không đưa thêm sai số (nhiễu) vào mô hình. 
    *   **Áp dụng Median Imputation:** Các ô đơn giá và tổng tiền bị khuyết còn lại (không thể khôi phục bằng công thức) được điền bằng **Median** của tập Train trong luồng xử lý chính (tạo ra bộ dữ liệu `ready`).

### Bước 2.2: Phục hồi tên mặt hàng (`Item`) bằng bản đồ liên kết
*   **Hành động:** Tạo một từ điển ánh xạ từ tập Train liên kết cặp khóa `(Category, Price)` sang tên sản phẩm `Item`. Sau đó tra cứu để điền các ô Item bị khuyết. Những ô còn lại được điền bằng Mode (mặt hàng bán chạy nhất).
*   **Lý do thực hiện:**
    *   Trong siêu thị, mỗi sản phẩm cụ thể thuộc một danh mục (`Category`) và có một mức giá cố định (`Price Per Unit`). Do đó, ta hoàn toàn có thể khôi phục lại tên mặt hàng gốc một cách chính xác dựa trên danh mục và đơn giá của nó.
    *   Điền khuyết bằng Mode ở cuối là giải pháp an toàn để xử lý triệt để các ô khuyết không thể tra cứu.

### Bước 2.3: Loại bỏ dòng khuyết nhãn mục tiêu (`Quantity`)
*   **Hành động:** Loại bỏ tất cả các dòng bị khuyết cột `Quantity`.
*   **Lý do thực hiện:**
    *   `Quantity` là nhãn mục tiêu (Target) chúng ta cần dự báo. Chúng ta không thể huấn luyện mô hình hồi quy giám sát nếu không có nhãn thực tế của dòng đó.

---

## Bước 3. Tạo Đặc Trưng Mới (Feature Creation)

### Bước 3.1: Trích xuất đặc trưng thời gian
*   **Hành động:** Tách cột `Transaction Date` thành 5 đặc trưng: `Year`, `Month`, `Day`, `DayOfWeek` (Thứ trong tuần), và `IsWeekend` (Cuối tuần - 0 hoặc 1).
*   **Lý do thực hiện:**
    *   Thời gian giao dịch dạng chữ gốc rất khó để thuật toán SVR học trực tiếp. Việc tách nhỏ giúp mô hình nhận diện các yếu tố chu kỳ (ví dụ: lượng mua sắm thường tăng mạnh vào cuối tuần hoặc các tháng lễ tết cuối năm).

### Bước 3.2: Đặc trưng tích lũy khách hàng (`Customer Aggregates`)
*   **Hành động:** Gom nhóm lịch sử mua sắm của từng khách hàng trên tập Train để tính: Tổng số lần mua hàng, Trung bình số lượng mua, và Trung bình số tiền chi tiêu (tính bằng Mean để phản ánh quy mô tiêu dùng trung bình).
*   **Áp dụng Median Imputation:** Đối với các khách hàng mới xuất hiện ở tập Test chưa có lịch sử mua hàng ở tập Train, các đặc trưng tích lũy bị khuyết này được điền bằng giá trị **Median** của các đặc trưng tích lũy từ tập Train (trong luồng xử lý chính).
*   **Lý do thực hiện:**
    *   Mã số khách hàng gốc (`Customer ID`) chỉ là một định danh dạng chữ/số phân loại, không có ý nghĩa toán học tuyến tính. 
    *   Để biến mã số này thành thông tin hữu ích, ta quy đổi nó thành hành vi tiêu dùng lịch sử của khách hàng đó.

### Bước 3.3: Mã hóa sản phẩm (`Target Encoding`) bằng Mean
*   **Hành động:** Thay thế tên sản phẩm (`Item`) và danh mục (`Category`) bằng trung bình lượng bán ra (`Quantity`) của chúng trên tập Train.
*   **Áp dụng Median Imputation:** Đối với các sản phẩm/danh mục mới xuất hiện ở tập Test chưa có ở tập Train, giá trị mã hóa bị khuyết này được điền bằng **Median** lượng bán ra của tập Train (trong luồng xử lý chính).
*   **Lý do thực hiện:**
    *   Cột tên sản phẩm có rất nhiều giá trị chữ khác nhau. Nếu dùng One-Hot Encoding sẽ làm phát sinh hàng trăm cột mới, gây loãng dữ liệu và làm SVM chạy cực kỳ chậm. Target Encoding giúp nén về 1 cột số duy nhất thể hiện sức bán chạy của sản phẩm đó.

---

## Bước 4. One-Hot Encoding
*   **Hành động:** Chuyển đổi các biến phân loại ít nhóm (`Payment Method`, `Location`) thành các cột nhị phân 0 và 1.

---

## Bước 5. Tạo 3 Kịch Bản Đặc Trưng (c1, c2, c3) & Chuẩn Hóa
*   **Hành động:** Thực hiện chuẩn hóa đồng loạt tất cả các cột số bằng `StandardScaler`, phân tách thành 3 kịch bản và xuất ra các file dữ liệu dạng **Median Imputation** (được ký hiệu là `ready`, `median_c2`, `median_c3`).

---

## Bước 6. Thực Thi Tự Động Hóa Xuất File Cho Bộ Điền Khuyết Mean (Đối Chứng)
*   **Hành động:** Chạy lại toàn bộ quy trình trên nhưng thay thế toàn bộ các bước điền khuyết thống kê (Imputation) từ Median sang **Mean** và lưu thành các file đối chứng (`mean_c1`, `mean_c2`, `mean_c3`).
*   **Lý do thực hiện:**
    *   Để có đầy đủ dữ liệu đối chứng phục vụ cho việc so sánh hiệu năng chi tiết giữa điền khuyết Mean và Median ở phần Modeling.

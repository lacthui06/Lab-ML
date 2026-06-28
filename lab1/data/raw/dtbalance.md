# 1. WHAT - Cân bằng dữ liệu là gì?
    Data Balance là trạng thái mà các lớp (classes) trong tập dữ liệu đích (Target/Label) có số lượng thực thể (samples) tương đương hoặc xấp xỉ bằng nhau.

    Tập dữ liệu cân bằng (Balanced): Tỷ lệ phân phối giữa các nhãn lý tưởng là 50/50, 45/55 hoặc 33/33/33 (đối với bài toán 3 nhãn).

    Tập dữ liệu mất cân bằng (Imbalanced): Có một lớp chiếm đại đa số (Majority class) và lớp còn lại chỉ chiếm một tỷ lệ rất nhỏ (Minority class) – giống như bài toán Email Spam của bạn.

# 2. WHY - Tại sao phải cần Data Balance?
    Nếu bạn mang một tập dữ liệu mất cân bằng nghiêm trọng đi huấn luyện (train) mô hình Machine Learning, bạn sẽ gặp tai họa mang tên "Bẫy độ chính xác" (Accuracy Paradox).

    Ví dụ thực tế: Tập dữ liệu có 990 email thường và 10 email spam.

    Nếu mô hình của bạn "lười biếng" và đoán bừa 100% tất cả đều là email thường, thì độ chính xác (Accuracy) của nó vẫn đạt tới 99%!

    Về mặt con số thì mô hình quá giỏi, nhưng về mặt thực tế thì nó vô dụng vì không lọc được bất kỳ một email spam nào. Mô hình bị thiên vị (bias) hoàn toàn vào lớp đa số.

    Do đó, cân bằng dữ liệu là để đảm bảo mô hình học đều các lớp, không bị "học lệch".

# 3. WHEN - Khi nào cần chú ý đến Data Balance?
    Bạn cần đặc biệt kiểm tra và xử lý sự cân bằng dữ liệu ở bước EDA (Phân tích khám phá) và Tiền xử lý (Data Preprocessing), ngay trước khi đưa dữ liệu vào train mô hình.

    Các bài toán thực tế luôn mặc định bị mất cân bằng dữ liệu mà bạn cần lưu ý:

    Phát hiện gian lận thẻ tín dụng (Triệu giao dịch mới có vài giao dịch gian lận).

    Chẩn đoán bệnh y khoa (Số người mắc bệnh hiểm nghèo luôn ít hơn người khỏe mạnh).

    Lọc email spam, phát hiện điều khoản bất thường trong văn bản pháp lý.

# 4. WHERE - Xử lý Data Balance ở đâu?
    Quá trình này diễn ra hoàn toàn trong Pipeline xử lý dữ liệu (Data Pipeline) của bạn trên code (Python, R, SQL...). Bạn có thể xử lý nó ở hai tầng:

    Tầng dữ liệu (Data-level): Can thiệp trực tiếp vào tập dataset (sử dụng thư viện như imblearn trong Python).

    Tầng thuật toán (Algorithm-level): Cấu hình ngay trong lúc gọi mô hình toán học (ví dụ thiết lập tham số class_weight='balanced' trong Scikit-learn).

# 5. WHICH - Những đối tượng nào bị ảnh hưởng và cần lựa chọn?

## a. Lớp dữ liệu nào (Which Classes) cần được cân bằng?
    Lớp Thiểu số (Minority Class): Là lớp có số lượng thực thể ít nhưng lại là mục tiêu cốt lõi cần phát hiện (ví dụ: nhãn "Spam" trong bài toán lọc thư rác, nhãn "Gian lận" trong giao dịch ngân hàng). Đây là lớp cần được tập trung cân bằng và theo dõi chỉ số.

## b. Tập dữ liệu phân hoạch nào (Which Data Partition) được phép cân bằng?
    Chỉ tập Huấn luyện (Train Set): Bạn CHỈ ĐƯỢC PHÉP thực hiện các kỹ thuật cân bằng dữ liệu (như SMOTE, Undersampling) trên tập Train.

    Tuyệt đối KHÔNG can thiệp tập Kiểm tra (Test/Validation Set): Tập Test phải được giữ nguyên trạng thái mất cân bằng tự nhiên để đánh giá khách quan nhất khả năng hoạt động của mô hình trong thực tế.

## c. Lựa chọn phương pháp xử lý dữ liệu (Resampling Method)
    Chọn SMOTE: Khi tập dữ liệu có kích thước nhỏ hoặc trung bình và bạn muốn tăng tính tổng quát hóa của mô hình mà không lo bị trùng lặp dữ liệu (Overfitting). Đây là lựa chọn mặc định phổ biến nhất.

    Chọn Undersampling: Khi tập dữ liệu cực kỳ khổng lồ (hàng triệu dòng) và việc huấn luyện mô hình tốn quá nhiều tài nguyên phần cứng.

    Chọn Class Weights (Trọng số lớp): Khi bạn muốn giữ nguyên cấu trúc phân phối tự nhiên của tập dữ liệu gốc mà không can thiệp vật lý vào dữ liệu. Rất phù hợp với Random Forest, SVM hoặc Logistic Regression.
## d. Thuật toán nào (Which Algorithms) nhạy cảm hoặc chống chịu tốt với mất cân bằng?
    Nhóm nhạy cảm cao (Sensitive): Logistic Regression, SVM, K-Nearest Neighbors (KNN), Neural Networks. Nhóm này rất dễ bị lệch hướng dự đoán về phía lớp đa số nếu dữ liệu không được cân bằng trước.

    Nhóm chống chịu tốt (Robust): Các mô hình dựa trên cây quyết định (Decision Tree, Random Forest, XGBoost, LightGBM). Các thuật toán này phân nhánh dựa trên độ tinh khiết (Purity) của các nút nên ít bị ảnh hưởng bởi tỷ lệ mất cân bằng toàn cục hơn.

# 6. HOW - Làm thế nào để đạt được Data Balance?
    Có 3 nhóm giải pháp chính để bạn "trị" bài toán mất cân bằng dữ liệu:

## a. Can thiệp vào Dữ liệu (Resampling)
    Undersampling (Cắt giảm): Xóa bớt ngẫu nhiên các dòng của lớp đa số để số lượng bằng lớp thiểu số. (Nhược điểm: Làm mất thông tin quý giá).

    Oversampling (Nhân bản): Sao chép ngẫu nhiên các dòng của lớp thiểu số cho nhiều lên. (Nhược điểm: Dễ gây Overfitting).

    SMOTE (Synthetic Minority Over-sampling Technique): Thuật toán tự sinh thêm các dữ liệu mới nhân tạo cho lớp thiểu số dựa trên các đặc trưng cũ, thay vì chỉ copy đè lên. Đây là cách cực kỳ phổ biến.

## b. Can thiệp vào Thuật toán (Cost-sensitive Learning)
    Sử dụng Class Weights: Trừng phạt mô hình thật nặng nếu nó đoán sai lớp thiểu số. Nói với mô hình: "Đoán sai 1 email spam sẽ bị trừ điểm nặng gấp 50 lần đoán sai 1 email thường".

## c. Thay đổi Tiêu chí đánh giá (Evaluation Metrics)
        Tuyệt đối không dùng Accuracy để đánh giá mô hình mất cân bằng.

        Thay vào đó, hãy dùng: Precision, Recall, F1-Score hoặc AUC-ROC. Các chỉ số này sẽ phản ánh chính xác xem mô hình thực sự nhận diện lớp thiểu số (Spam) tốt hay tồi.
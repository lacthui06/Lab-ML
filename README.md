# 🧠 Machine Learning & Deep Learning Labs (Lab-ML)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter" />
  <img src="https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white" alt="LaTeX" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

---

## 📖 Giới Thiệu Tổng Quan

**Lab-ML** là kho lưu trữ toàn diện tập hợp **5 đề tài nghiên cứu & thực hành Machine Learning / Deep Learning** chuẩn mực. Dự án được xây dựng với mục tiêu bao quát trọn vẹn vòng đời phát triển một hệ thống học máy (End-to-End Machine Learning Lifecycle):

1. **Khám phá & Trực quan hóa dữ liệu (Exploratory Data Analysis - EDA)**
2. **Kỹ thuật trích xuất & Xử lý đặc trưng (Feature Engineering)**
3. **Huấn luyện, Đánh giá & Tối ưu mô hình (Modeling & Evaluation)**
4. **Triển khai ứng dụng Web tương tác (Interactive Deployment with Streamlit)**
5. **Biên soạn Báo cáo học thuật tự động bằng LaTeX (Automated Academic Reporting Engine)**

---

## 🎯 Tổng Hợp 5 Đề Tài / Dự Án Trọng Tâm

| Dự Án | Lĩnh Vực / Bài Toán | Thuật Toán & Kỹ Thuật Chính | Bộ Dữ Liệu | Sản Phẩm / Điểm Nổi Bật |
| :--- | :--- | :--- | :--- | :--- |
| **Lab 1** | **Email Spam Detection**<br>*(Phân loại Thư rác)* | NLP, TF-IDF Vectorization, Logistic Regression | `CEAS_08` Dataset | Ứng dụng Streamlit dự đoán thư rác theo thời gian thực |
| **Lab 2** | **Predicting Product Sales**<br>*(Dự đoán Doanh số)* | Regression, Support Vector Regression (SVR), Scaling Pipeline | Dữ liệu giao dịch sản phẩm | Mô hình SVR tối ưu hóa siêu tham số + Web Demo |
| **Lab 3** | **Customer Segmentation**<br>*(Phân khúc Khách hàng)* | Unsupervised Learning, K-Means Clustering, Elbow Method | `Mall Customers` Dataset | Web App phân nhóm khách hàng + **Bonus: Image Segmentation (K-Means)** |
| **Lab 4** | **Housing Price Prediction**<br>*(Dự đoán Giá nhà)* | Deep Learning, Multilayer Perceptron (MLP), Backpropagation | `California Housing` Dataset | Thử nghiệm sâu các kịch bản mạng nơ-ron (PA1, PA2, PA3_A, PA3_B) |
| **Báo Cáo** | **Hệ Thống LaTeX Tự Động**<br>*(Academic Report Engine)* | Biên dịch XeLaTeX qua Python, Tự động escape cú pháp | Báo cáo chuyên sâu 4 Labs | Xuất file `report.pdf` chuẩn học thuật kèm 50+ biểu đồ phân tích |

---

## 🔬 Chi Tiết Các Dự Án

### 📩 Lab 1: Phát Hiện Thư Rác (Email Spam Classification)
* **Mục tiêu:** Xây dựng mô hình phân loại email độc hại / spam với độ chính xác cao.
* **Pipeline:**
  * **EDA:** Phân tích độ dài văn bản, tần suất xuất hiện của từ khóa spam, cân bằng dữ liệu.
  * **Feature Engineering:** Làm sạch văn bản, chuẩn hóa token, vector hóa bằng TF-IDF và lưu trữ pipeline tiền xử lý `preprocess_pack.pkl`.
  * **Modeling:** Huấn luyện mô hình Logistic Regression đạt độ hội tụ cao.
  * **Web Demo:** Giao diện Streamlit cho phép người dùng nhập trực tiếp nội dung email để kiểm tra.
  * *Chạy ứng dụng:* `streamlit run lab1/app_streamlit.py`

---

### 📈 Lab 2: Dự Đoán Doanh Số Sản Phẩm (Product Sales Prediction)
* **Mục tiêu:** Dự báo doanh số bán hàng của sản phẩm dựa trên các chỉ số tiếp thị và đặc tính thị trường.
* **Pipeline:**
  * **EDA:** Khám phá phân phối dữ liệu, phát hiện ngoại lai (outliers), phân tích tương quan Pearson/Spearman.
  * **Feature Engineering:** Chuẩn hóa dữ liệu với `StandardScaler`, xử lý biến định tính, lưu trữ `scaler_c1.pkl`.
  * **Modeling:** Huấn luyện thuật toán Support Vector Machine (SVR), tinh chỉnh Kernel và hệ số phạt $C$.
  * **Web Demo:** Giao diện nhập thông số sản phẩm và dự đoán doanh số tức thì.
  * *Chạy ứng dụng:* `streamlit run lab2/app.py`

---

### 👥 Lab 3: Phân Khúc Khách Hàng & Phân Vùng Ảnh (Customer & Image Segmentation)
* **Mục tiêu:** Khám phá các nhóm khách hàng mục tiêu để tối ưu chiến dịch marketing (Unsupervised Learning).
* **Pipeline:**
  * **EDA:** Trực quan hóa mối quan hệ giữa Độ tuổi, Thu nhập hàng năm (Annual Income) và Điểm chi tiêu (Spending Score).
  * **Modeling:** Áp dụng K-Means Clustering, xác định số cụm tối ưu $K$ qua phương pháp Elbow và Silhouette Score.
  * **Bonus Mở rộng:** Thử nghiệm thuật toán K-Means ứng dụng trong **Phân vùng màu sắc hình ảnh (Image Color Quantization & Segmentation)** tại notebook `image_segmentation.ipynb`.
  * **Web Demo:** Ứng dụng phân nhóm khách hàng tương tác trực quan.
  * *Chạy ứng dụng:* `streamlit run lab3/app.py`

---

### 🏡 Lab 4: Dự Đoán Giá Nhà Bằng Mạng Nơ-ron Sâu (California Housing Price using Deep MLP)
* **Mục tiêu:** Dự báo giá trị nhà ở trung bình tại California bằng mạng nơ-ron truyền thẳng nhiều tầng (Multilayer Perceptron).
* **Pipeline:**
  * **EDA & Feature Engineering:** Xử lý địa lý (Kinh độ/Vĩ độ), tương quan phòng ở, chuẩn hóa dữ liệu đầu vào.
  * **Kiến trúc thử nghiệm (Experiment Matrix):**
    * `PA1`: Mô hình cơ sở (Baseline MLP).
    * `PA2`: Thử nghiệm các hàm kích hoạt (ReLU, LeakyReLU, ELU) và độ sâu mạng.
    * `PA3_A` & `PA3_B`: Áp dụng kỹ thuật chống Overfitting (Dropout, Batch Normalization, L2 Regularization, Early Stopping).
  * **Tối ưu hóa:** Đánh giá độ hội tụ của hàm mất mát (Loss Curve) và chỉ số $R^2$, RMSE trên tập Test.

---

### 📄 Hệ Thống Báo Cáo Học Thuật LaTeX (Automated Report Engine)
* **Điểm đột phá:** Tích hợp pipeline biên dịch báo cáo tự động từ Python sang XeLaTeX.
* **Đặc điểm:**
  * Giảm thiểu lỗi cú pháp ký tự đặc biệt (`_`) trong LaTeX.
  * Tích hợp hơn 50 đồ thị trực quan hóa chất lượng cao từ thư mục `report/figures/`.
  * Định dạng chuẩn bài báo/tiểu luận khoa học (Mục lục, Danh mục hình ảnh, Danh mục bảng biểu, Font chữ Times New Roman/Computer Modern, giãn dòng chuẩn).
  * *Biên dịch báo cáo:* Chạy lệnh `python report/generate_huge_report.py` (hoặc `compile_report.py`).

---

## 📂 Cấu Trúc Thư Mục Repository

Dự án được tổ chức đồng bộ và chuyên nghiệp theo cấu trúc mô-đun:

```plaintext
Lab-ML/
│
├── lab1/                     # Đề tài 1: Phân loại Email Spam
│   ├── data/                 # Dữ liệu gốc (raw) và tiền xử lý (ready_train)
│   ├── eda/                  # Notebook và cẩm nang phân tích dữ liệu
│   ├── feature egineer/      # Trích xuất đặc trưng & pipeline tiền xử lý
│   ├── modeling/             # Huấn luyện Logistic Regression & Model pkl
│   └── app_streamlit.py      # Ứng dụng Web Demo Streamlit
│
├── lab2/                     # Đề tài 2: Dự đoán Doanh số Sản phẩm
│   ├── eda/                  # Phân tích & Trực quan hóa dữ liệu
│   ├── feature_engineer/     # Chuẩn hóa dữ liệu & Scaler
│   ├── modeling/             # Huấn luyện Support Vector Machine (SVM)
│   └── app.py                # Ứng dụng Web Demo Streamlit
│
├── lab3/                     # Đề tài 3: Phân khúc Khách hàng & Phân vùng ảnh
│   ├── data/                 # Dataset Shopping Mall Customer
│   ├── eda/                  # Phân tích khám phá cụm dữ liệu
│   ├── modeling/             # K-Means Clustering & Trọng tâm cụm
│   ├── additional/           # Bài toán mở rộng: Image Segmentation
│   └── app.py                # Ứng dụng Web Demo Streamlit
│
├── lab4/                     # Đề tài 4: Mạng Nơ-ron Deep MLP (Housing Price)
│   ├── data/                 # California Housing Dataset & 4 bộ phân chia thử nghiệm
│   ├── eda/                  # Phân tích tương quan thuộc tính nhà
│   ├── feature egineer/      # Kỹ thuật tiền xử lý cho mạng sâu
│   └── modeling/             # Huấn luyện mô hình MLP trên Kaggle & Notebook
│
├── report/                   # Hệ thống Báo cáo Khoa học hoàn chỉnh
│   ├── figures/              # Chứa hơn 50 biểu đồ trực quan hóa
│   ├── generate_huge_report.py # Script sinh mã nguồn LaTeX
│   ├── report.tex            # File nguồn LaTeX
│   └── report.pdf            # Bản báo cáo học thuật hoàn chỉnh (PDF)
│
├── .gitignore                # Quản lý loại trừ file rác Git
└── README.md                 # Tài liệu giới thiệu dự án
```

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Sao chép kho lưu trữ (Clone Repository)

```bash
git clone https://github.com/lacthui06/Lab-ML.git
cd Lab-ML
```

### 2. Thiết lập Môi trường ảo (Virtual Environment)

```bash
# Tạo môi trường ảo với Python
python -m venv venv

# Kích hoạt môi trường (Windows)
venv\Scripts\activate

# Kích hoạt môi trường (macOS / Linux)
source venv/bin/activate
```

### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 4. Khởi chạy các Ứng dụng Web Demo

Bạn có thể chạy thử nghiệm trực tiếp giao diện người dùng của từng bài Lab:

* **Chạy Web Demo Spam Email (Lab 1):**
  ```bash
  streamlit run lab1/app_streamlit.py
  ```
* **Chạy Web Demo Dự đoán Doanh số (Lab 2):**
  ```bash
  streamlit run lab2/app.py
  ```
* **Chạy Web Demo Phân khúc Khách hàng (Lab 3):**
  ```bash
  streamlit run lab3/app.py
  ```

---

## 🛠️ Công Nghệ & Công Cụ Sử Dụng

| Nhóm Công Nghệ | Công Cụ / Thư Viện |
| :--- | :--- |
| **Ngôn ngữ chính** | Python 3.10+ |
| **Khoa học Dữ liệu & Học máy** | NumPy, Pandas, Scikit-learn, SciPy |
| **Trực quan hóa Dữ liệu** | Matplotlib, Seaborn |
| **Giao diện & Web App** | Streamlit |
| **Môi trường Thực nghiệm** | Jupyter Notebook, Kaggle GPU |
| **Hệ thống Soạn thảo Học thuật**| LaTeX, XeLaTeX, TeX Live |

---

## 👥 Tác Giả & Đội Ngũ Thực Hiện (Contributors)

Dự án được xây dựng và hoàn thiện bởi sự phối hợp giữa tác giả chính và Trợ lý Lập trình AI Thông minh:

<table align="center">
  <tr>
    <td align="center" width="220">
      <a href="https://github.com/lacthui06">
        <img src="https://github.com/lacthui06.png" width="100px;" alt="Thái Anh Lạc"/><br />
        <sub><b>Thái Anh Lạc</b></sub>
      </a><br />
      <sub>👑 Lead Developer & Author</sub><br />
      <a href="mailto:thaianhlac06@gmail.com">✉️ thaianhlac06@gmail.com</a>
    </td>
    <td align="center" width="220">
      <a href="https://deepmind.google">
        <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" width="100px;" alt="Antigravity"/><br />
        <sub><b>Antigravity</b></sub>
      </a><br />
      <sub>🤖 AI Co-Contributor & Companion</sub><br />
      <sub>Google DeepMind Agentic AI</sub>
    </td>
  </tr>
</table>

---

## 📝 Giấy Phép (License)

Dự án này được phân phối dưới giấy phép **MIT License**. Bạn hoàn toàn có thể tự do tham khảo, học tập và phát triển thêm.

<p align="center">
  <i>Cảm ơn bạn đã ghé thăm dự án! Nếu thấy hữu ích, đừng quên để lại một ⭐️ Star để ủng hộ chúng tôi nhé!</i>
</p>

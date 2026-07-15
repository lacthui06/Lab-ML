# Hướng dẫn Biên soạn Tiểu luận & Báo cáo Học thuật Tối ưu (LaTeX + Python)

Tài liệu này đúc kết phương pháp luận tối ưu hóa hiệu năng, giảm thiểu lượng token tiêu thụ khi làm việc với AI, và quy trình biên soạn báo cáo khoa học chất lượng cao bằng hệ thống XeLaTeX.

---

## I. Phương pháp luận Tối ưu hóa Token & Hiệu năng

Khi thực hiện các báo cáo lớn hoặc tiểu luận học thuật (từ 50 - 100+ trang), việc nạp toàn bộ mã nguồn hoặc dữ liệu thô vào ngữ cảnh AI sẽ gây lãng phí token cực kỳ lớn và làm giảm độ chính xác của phản hồi. 

### 1. Nguyên tắc Trích xuất Thông tin Mục tiêu (Targeted Extraction)
*   **Không đọc toàn bộ notebook dạng thô:** Thay vào đó, hãy viết các script Python cào cấu trúc file `.ipynb` (JSON) để chỉ lấy ra code của các cell quan trọng (ví dụ: các class mô hình tự viết, hàm train chính, hoặc các cell xuất ra chỉ số metric).
*   **Harvesting kết quả đầu ra:** Chỉ lưu trữ các kết quả in ra màn hình (`stdout`) dưới dạng tóm tắt hoặc ghi file text ngắn gọn (`extracted_text_outputs.txt`), loại bỏ hoàn toàn các dòng log lặp đi lặp lại của epoch training.

### 2. Thiết kế Cấu trúc Báo cáo Phân cấp (Modular LaTeX Template)
*   Sử dụng một file Python trung gian (`generate_huge_report.py`) để chứa nội dung thô và các định nghĩa bảng biểu dạng chuỗi raw string (`r"""..."""`).
*   **Tại sao lại dùng Python để viết LaTeX?**
    *   Giúp lập trình hóa các cấu trúc lặp đi lặp lại (ví dụ: tạo hàng loạt trang mục lục, lặp qua danh sách hình ảnh).
    *   Dễ dàng áp dụng các hàm xử lý văn bản (regex) để tự động sửa lỗi cú pháp trước khi ghi ra file `.tex`.
    *   Hạn chế tối đa việc AI phải viết lại toàn bộ file LaTeX hàng trăm dòng khi chỉ cần sửa một vài từ.

### 3. Tự động hóa Dọn dẹp và Biên dịch (Compilation Automation)
*   Viết một kịch bản biên dịch chạy XeLaTeX 2-3 lần để tự động đồng bộ hóa Mục lục (TOC), Danh mục hình ảnh (LOF), Danh mục bảng biểu (LOT) và các tham chiếu chéo (`\ref{}`, `\cite{}`).
*   Luôn tích hợp bước xóa cache để tránh việc biên dịch bị đứng do file phụ trợ (`.aux`, `.toc`) bị hỏng từ các lần biên dịch lỗi trước đó.

---

## II. Quy trình Từng bước Thiết lập Tiểu luận Mới (Implementation Plan)

### Bước 1: Chuẩn bị Thư mục & Hình ảnh
1.  Tạo cấu trúc thư mục dự án chuẩn:
    ```
    ├── figures/              # Chứa toàn bộ hình ảnh, biểu đồ xuất ra từ notebook
    ├── data/                 # Dữ liệu raw và processed
    ├── notebooks/            # Các file Jupyter Notebook chạy thực nghiệm
    ├── generate_report.py    # File Python sinh mã LaTeX
    └── compile_report.py     # Script biên dịch tự động
    ```
2.  Đảm bảo tất cả các hình ảnh xuất ra từ matplotlib/seaborn đều được đặt tên nhất quán và lưu dưới dạng `.png` hoặc `.jpg` trong thư mục `figures/` (ví dụ: `lab1_eda_fig1.png`).

### Bước 2: Viết Template LaTeX trong Python (`generate_report.py`)
Sử dụng cấu trúc khung LaTeX tiêu chuẩn sau để đảm bảo thẩm mỹ học thuật chuyên nghiệp:
```python
# -*- coding: utf-8 -*-
latex_template = r"""\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english]{babel}
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{float}
\usepackage{caption}
\usepackage{setspace}
\setstretch{1.6} % Tạo khoảng cách dòng kép giúp báo cáo thoáng, dễ đọc
\usepackage{tocloft}
\usepackage{titlesec}

% Định dạng tiêu đề chương/phần chuyên nghiệp
\titleformat{\section}{\normalfont\Large\bfseries\color{blue}\centering}{\thesection}{1em}{}

% Cấu hình TOC/LOF/LOT tránh đè chữ
\renewcommand{\cftfigpresnum}{Figure~}
\renewcommand{\cfttabpresnum}{Table~}
\setlength{\cftfignumwidth}{2.5cm}
\setlength{\cfttabnumwidth}{2.3cm}

\begin{document}
% Nội dung trang bìa, mục lục và các chương nằm ở đây
\end{document}
"""
```

### Bước 3: Quy tắc Quản lý Ký tự Đặc biệt (Underscore Rules)
*   **Trong văn bản thường:** Mọi ký tự gạch dưới `_` nằm ngoài môi trường code hoặc listings đều phải được viết dưới dạng `\_` để tránh LaTeX hiểu lầm là bắt đầu ký hiệu toán học chỉ số dưới (Subscript).
*   **Trong nhãn và tham chiếu:** Các lệnh `\label{...}`, `\ref{...}`, `\includegraphics{...}` và `\url{...}` **bắt buộc phải giữ nguyên ký tự gạch dưới thô `_`**. Việc viết `\label{fig\_1}` sẽ làm hỏng file `.aux` và khiến trình biên dịch báo lỗi `Extra \endcsname`.
*   **Trong Listings/Verbatim:** Giữ nguyên `_` thô, không được escape.

### Bước 4: Viết Script Biên dịch Tự động (`compile_report.py`)
Sử dụng script Python dưới đây để thực hiện dọn dẹp cache và biên dịch XeLaTeX an toàn:
```python
import os
import subprocess

def clean_and_compile():
    # 1. Xóa toàn bộ file cache cũ để tránh xung đột
    extensions = [".aux", ".toc", ".lof", ".lot", ".out", ".log"]
    for ext in extensions:
        if os.path.exists(f"report{ext}"):
            os.remove(f"report{ext}")
            print(f"Deleted report{ext}")

    # 2. Biên dịch lần 1 để tạo cấu trúc aux và toc
    print("Compiling Pass 1...")
    subprocess.run(["xelatex", "-interaction=nonstopmode", "report.tex"])

    # 3. Biên dịch lần 2 để cập nhật số trang vào mục lục
    print("Compiling Pass 2...")
    subprocess.run(["xelatex", "-interaction=nonstopmode", "report.tex"])

    # 4. Biên dịch lần 3 để ổn định hoàn toàn liên kết
    print("Compiling Pass 3...")
    subprocess.run(["xelatex", "-interaction=nonstopmode", "report.tex"])

if __name__ == "__main__":
    clean_and_compile()
```

---

## III. Hướng dẫn Dọn dẹp File trong Thư mục Dự án

Sau khi hoàn thành báo cáo và xuất ra file PDF thành công, thư mục của bạn sẽ chứa rất nhiều file trung gian. Dưới đây là bảng phân loại chi tiết các đuôi file và khuyến nghị xử lý:

| Đuôi file | Tên file ví dụ | Vai trò trong hệ thống | Khuyến nghị Xử lý |
| :--- | :--- | :--- | :--- |
| **.pdf** | `report.pdf` | File tài liệu đầu ra cuối cùng phục vụ nộp bài. | **BẮT BUỘC GIỮ** |
| **.tex** | `report.tex` | Mã nguồn LaTeX của báo cáo. | **BẮT BUỘC GIỮ** |
| **.py** | `generate_huge_report.py` | Script Python tự động sinh file `.tex`. | **NÊN GIỮ** (để tái sinh hoặc chỉnh sửa hàng loạt sau này) |
| **.docx** | `trang_bia.docx` | File Word mẫu trang bìa ban đầu. | **ĐÃ HẾT GIÁ TRỊ** (Có thể xóa hoặc lưu trữ dạng lưu niệm) |
| **.txt** | `extracted_text_outputs.txt` | File chứa log chạy code thô để copy vào báo cáo. | **CÓ THỂ XÓA** (vì thông tin đã được viết vào báo cáo) |
| **.aux** | `report.aux` | File phụ trợ chứa thông tin nhãn (labels) và liên kết chéo. | **XÓA KHÔNG ẢNH HƯỞNG** (Sẽ tự tạo lại khi biên dịch) |
| **.toc** | `report.toc` | File cache lưu trữ cấu trúc Mục lục (Table of Contents). | **XÓA KHÔNG ẢNH HƯỞNG** (Sẽ tự tạo lại khi biên dịch) |
| **.lof** | `report.lof` | File cache lưu trữ Danh mục hình ảnh (List of Figures). | **XÓA KHÔNG ẢNH HƯỞNG** (Sẽ tự tạo lại khi biên dịch) |
| **.lot** | `report.lot` | File cache lưu trữ Danh mục bảng biểu (List of Tables). | **XÓA KHÔNG ẢNH HƯỞNG** (Sẽ tự tạo lại khi biên dịch) |
| **.out** | `report.out` | File cache phục vụ việc tạo bookmark mục lục trong file PDF. | **XÓA KHÔNG ẢNH HƯỞNG** (Sẽ tự tạo lại khi biên dịch) |
| **.log** | `report.log` | File nhật ký ghi lại toàn bộ tiến trình biên dịch LaTeX. | **XÓA KHÔNG ẢNH HƯỞNG** (Chỉ dùng để debug khi lỗi) |

### Lời khuyên khi dọn dẹp:
1.  **Dọn dẹp trước khi nén bài nộp:** Khi nộp mã nguồn cho giảng viên hoặc lưu trữ lên GitHub, hãy **xóa toàn bộ các file cache** (`.aux`, `.toc`, `.lof`, `.lot`, `.out`, `.log`). Điều này giúp thư mục gọn gàng, giảm dung lượng nén từ hàng chục MB xuống chỉ còn vài KB mã nguồn sạch.
2.  **Cách dọn nhanh bằng Command Line:**
    Trong thư mục dự án, bạn có thể chạy lệnh PowerShell sau để dọn dẹp sạch sẽ cache:
    ```powershell
    Remove-Item report.aux, report.out, report.toc, report.lof, report.lot, report.log -ErrorAction SilentlyContinue
    ```

# LaTeX Report Generation and Compilation Skill (skill-tex-pdf)

Tài liệu này định nghĩa kỹ năng và quy trình chuẩn (skill) để biên soạn và biên dịch báo cáo học thuật bằng LaTeX bằng cách sử dụng script Python. Các tác vụ sau này của AI đối với dự án LaTeX lớn cần đọc và tuân thủ các quy tắc trong tài liệu này để tối ưu hóa hiệu năng, giảm thiểu lượng token tiêu thụ và tăng tốc độ xử lý.

---

## 1. Nguyên Tắc Lõi (Core Principles)

*   **Tại sao hoạt động qua file `.py` đỡ hao quota (token) hơn file `.tex` trực tiếp?**
    *   **Giảm thiểu việc ghi đè văn bản lớn:** File `.tex` hoàn chỉnh rất nặng (~120KB, gần 2000 dòng). Nếu AI làm việc trực tiếp trên file `.tex`, mỗi khi bạn yêu cầu sửa đổi nhỏ (ví dụ: sửa một câu ở trang 80), AI thường phải đọc và viết lại một lượng lớn code LaTeX xung quanh trong phản hồi chat, gây hao tổn hàng chục ngàn token đầu ra (output tokens) và dễ bị lỗi hàng chờ.
    *   **Chỉnh sửa mục tiêu bằng Python:** Khi gom mã nguồn vào chuỗi `latex_code` của `generate_huge_report.py`, AI chỉ cần sử dụng công cụ thay thế khối (`replace_file_content`) để thực hiện các thay đổi cực kỳ nhỏ trên file `.py` (chỉ mất vài chục token). Việc sinh ra file `.tex` đầy đủ 2000 dòng sẽ do máy tính của bạn chạy biên dịch tự động đảm nhiệm, hoàn toàn miễn phí quota.
    *   **Tự động hóa sửa lỗi cú pháp:** Trình biên dịch Python có thể tự sửa lỗi gạch dưới `_` hàng loạt trên toàn bộ 2000 dòng văn bản trong nháy mắt, điều mà AI nếu làm thủ công trên file `.tex` sẽ tốn rất nhiều lượt chat (quota) để debug.

*   **Quy tắc Escape dấu gạch dưới (`_`):**
    *   Trong văn bản thường, tiêu đề, bảng biểu, công thức toán học: Bắt buộc phải được escape thành `\_`.
    *   Trong nhãn liên kết và tài nguyên: `\label{...}`, `\ref{...}`, `\includegraphics{...}`, và `\url{...}` **bắt buộc phải giữ nguyên dạng `_` thô** (không escape).
    *   Trong môi trường code: `lstlisting` và `verbatim` **bắt buộc phải giữ nguyên dạng `_` thô** (không escape).

---

## 2. Quy Chuẩn Định Dạng Báo Cáo Học Thuật (Format Standards)

Báo cáo cần tuân thủ cấu trúc định dạng chuẩn của các bài tiểu luận lớn theo quy cách sau:

### 2.1. Cấu hình Trang và Font chữ (Geometry & Typography)
*   **Phân biệt Chữ có chân (Serif) và Chữ không chân (Sans-Serif):**
    *   **Chữ có chân (Serif):** Là những kiểu chữ có các nét gạch nhỏ trang trí (gọi là "serif") ở phần đầu hoặc đuôi của các nét chính. Ví dụ: *Times New Roman, Georgia, Garamond, Computer Modern*. Font Serif tạo hiệu ứng liên kết từ dòng này sang dòng khác, giúp mắt đọc lướt nhanh hơn trên văn bản in ấn dài.
    *   **Chữ không chân (Sans-Serif):** ("Sans" trong tiếng Pháp nghĩa là "không có"). Đây là những kiểu chữ tối giản, các nét chữ thẳng đứng, sạch sẽ, không có nét gạch trang trí ở đầu/đuôi nét. Ví dụ: *Arial, Helvetica, Calibri, Inter, Roboto*. Font Sans-serif mang cảm giác hiện đại, dễ đọc trên màn hình điện tử hoặc khi hiển thị chữ kích thước nhỏ (như nhãn biểu đồ, trục đồ thị).
*   **Kiểu chữ chủ đạo (Font Family):** Tùy thuộc vào yêu cầu tạp chí/trường học. Mặc định ưu tiên chọn font có chân `Times New Roman` cho báo cáo thường, hoặc font mặc định LaTeX cho bài toán lý thuyết.
*   **Cỡ chữ và phân cấp tiêu đề (Font Size Hierarchy):** Tiêu đề và nội dung bắt buộc phải có kích thước khác nhau để tạo cấu trúc phân cấp trực quan rõ ràng:
    *   *Tiêu đề bài báo chính (Main Title):* 24pt, in đậm, căn giữa (`\fontsize{24}{28}\selectfont\textbf{...}`).
    *   *Tiêu đề phụ chính (Subtitle):* 18pt, in đậm, căn giữa (`\fontsize{18}{22}\selectfont\textbf{...}`).
    *   *Tiêu đề mục lớn (Section - Chap 1, 2, ...):* `\Large` (tương đương 14.4pt), in đậm, màu xanh đậm hoặc đen (`\titleformat{\section}{\normalfont\Large\bfseries...}`).
    *   *Tiêu đề mục con (Subsection - 1.1, 1.2, ...):* `\large` (tương đương 12pt), in đậm (`\titleformat{\subsection}{\normalfont\large\bfseries...}`).
    *   *Tiêu đề mục nhỏ (Sub-subsection - 1.1.1, ...):* `\normalsize` (tương đương 12pt), in đậm (`\titleformat{\subsubsection}{\normalfont\normalsize\bfseries...}`).
    *   *Chữ thân bài (Body Text):* 12pt (đặt ở tùy chọn `\documentclass[12pt,a4paper]{article}`).
*   **Cỡ chữ thân bài (Body Text Size):** 12pt.
*   **Căn lề dòng (Line Spacing):** Căn lề giãn dòng 1.5 (sử dụng gói `setspace` và khai báo lệnh `\setstretch{1.5}`).
*   **Căn lề trang (Margins):** 
    *   Trang đứng A4.
    *   Căn lề trên (Top) và dưới (Bottom) là 1.5 inch (hoặc theo quy chuẩn hình học: `\usepackage[a4paper, top=3.8cm, bottom=3.8cm, left=3cm, right=2.5cm]{geometry}`).
*   **Dàn trang (Justification):** Văn bản chính phải được dàn đều 2 bên (LaTeX mặc định tự động dàn đều hai bên - justified, không sử dụng các lệnh căn trái/phải trừ khi viết tiêu đề).

---

## 2.1.B. Quy Định Tương Tác Trắc Nghiệm Của AI (AI Interactive Survey)
**BẮT BUỘC:** Mỗi khi người dùng bắt đầu một yêu cầu viết báo cáo/tiểu luận mới, AI **không được tự ý quyết định kiểu chữ** mà phải gọi công cụ `ask_question` để hiển thị hộp thoại trắc nghiệm cho người dùng lựa chọn cấu hình tài liệu mong muốn:
1.  **Lựa chọn Kiểu Font chữ chính:**
    *   *Option 1:* "Times New Roman (Có chân - Serif, Chuẩn học thuật truyền thống)"
    *   *Option 2:* "Computer Modern (Có chân - Serif, Mặc định của LaTeX cho Toán/Tin)"
    *   *Option 3:* "Arial / Helvetica (Không chân - Sans-serif, Phong cách hiện đại/tối giản)"
2.  **Lựa chọn Giãn dòng (Line Spacing):**
    *   *Option 1:* "Giãn dòng 1.5 (Tiêu chuẩn tiểu luận/báo cáo)"
    *   *Option 2:* "Giãn dòng 1.6 (Cực kỳ thoáng, dễ đọc bản nháp)"
    *   *Option 3:* "Giãn dòng đơn 1.0 (Tiết kiệm trang giấy)"
3.  **Lựa chọn Lề trang (Geometry Margins):**
    *   *Option 1:* "Lề chuẩn 2.5cm đều 4 bên"
    *   *Option 2:* "Lề rộng học thuật (Top/Bottom 1.5 inch, Left/Right 1 inch)"
    *   *Option 3:* "Lề hẹp 2.0cm (Để chứa các bảng dữ liệu lớn)"

### 2.2. Bố cục và các loại Mục lục (Table of Contents & Lists)
Tài liệu phải chứa đầy đủ 3 loại mục lục ở các trang đầu tiên sau trang bìa và lời cảm ơn, mỗi danh mục nằm trên một trang riêng biệt (`\newpage`):
1.  **Mục lục chính (Table of Contents):** Gọi lệnh `\tableofcontents`. Các chương phải định dạng tiền tố rõ ràng như `Chap 1 - ...`, `Chap 2 - ...` (cấu hình qua `titlesec`).
2.  **Danh mục hình ảnh (List of Figures):** Gọi lệnh `\listoffigures`.
3.  **Danh mục bảng biểu (List of Tables):** Gọi lệnh `\listoftables`.
*   *Lưu ý cấu hình danh mục:* Để tránh chồng lấn chữ khi số thứ tự hình/bảng lớn, bắt buộc khai báo cấu hình `tocloft` trong preamble để tự động chèn chữ "Figure " hoặc "Table " trước số thứ tự trong danh mục:
    ```latex
    \renewcommand{\cftfigpresnum}{Figure~}
    \renewcommand{\cfttabpresnum}{Table~}
    \setlength{\cftfignumwidth}{2.5cm}
    \setlength{\cfttabnumwidth}{2.3cm}
    ```

### 2.3. Quy chuẩn chèn Hình ảnh (Figures)
*   Mọi hình ảnh phải nằm trong môi trường `\begin{figure}[H] ... \end{figure}` (sử dụng gói `float` để ép ảnh hiển thị đúng vị trí trong text).
*   **Căn giữa ảnh:** Bắt buộc có lệnh `\centering` ngay sau lệnh begin.
*   **Kích thước ảnh:** Giới hạn chiều rộng ở mức phù hợp (ví dụ: `[width=0.95\textwidth]`).
*   **Chú thích hình ảnh (Caption):** Lệnh `\caption{...}` phải đặt ở **phía dưới** hình ảnh.
*   **Nhãn liên kết:** Đặt `\label{fig:label_name}` ngay dưới caption để tham chiếu bằng `Figure~\ref{fig:label_name}`.

### 2.4. Quy chuẩn chèn Bảng biểu (Tables)
*   Mọi bảng dữ liệu phải nằm trong môi trường `\begin{table}[H] ... \end{table}`.
*   **Căn giữa bảng:** Bắt buộc có `\centering`.
*   **Chống tràn viền (Responsive Table):** Mọi bảng có độ rộng lớn bắt buộc phải được bao bọc bởi lệnh tự co dãn:
    ```latex
    \resizebox{\textwidth}{!}{
        \begin{tabular}{...}
        ...
        \end{tabular}
    }
    ```
*   **Chú thích bảng biểu:** Lệnh `\caption{...}` đối với bảng biểu bắt buộc phải được đặt ở **phía trên** bảng biểu.
*   **Thẩm mỹ dòng kẻ:** Sử dụng gói `booktabs` với các đường kẻ sang trọng: `\toprule` (đường kẻ đầu bảng), `\midrule` (đường kẻ ngăn tiêu đề), và `\bottomrule` (đường kẻ đáy bảng). Không lạm dụng các đường kẻ dọc gây rối mắt.

### 2.5. Kỹ Thuật Viết Tránh Đạo Văn và Vượt Qua Bộ Quét AI (Anti-Plagiarism & Human-like Writing)
Để vượt qua các bộ kiểm tra đạo văn (như Turnitin) và bộ quét AI Detector (như GPTZero, Copyleaks), AI và người dùng cần tuân thủ các quy tắc hành văn sau:
*   **Tránh Đạo văn (Anti-Plagiarism):**
    *   *Diễn đạt lại đa nguồn (Paraphrasing):* AI tự động chuyển đổi cấu trúc câu (chuyển câu chủ động/bị động), sử dụng các từ đồng nghĩa phù hợp ngữ cảnh để diễn đạt lại ý tưởng thay vì sao chép nguyên văn.
    *   *Trích dẫn chuẩn hóa (Citation):* Mọi nguồn thông tin/định nghĩa tham khảo phải được dẫn nguồn rõ ràng bằng lệnh `\cite{...}` hoặc footnote. Các câu trích dẫn nguyên văn bắt buộc đặt trong môi trường `quote`.
*   **Vượt qua bộ quét AI (Bypassing AI Detectors):**
    *   *Biến động độ dài câu (High Burstiness):* Hành văn đan xen linh hoạt giữa các câu rất ngắn (để nhấn mạnh luận điểm) và câu dài phức tạp (để giải thích chiều sâu). Tránh viết các câu có cấu trúc và độ dài đều nhau.
    *   *Từ bỏ từ nối rập khuôn:* Tuyệt đối không dùng các từ nối đặc trưng của AI như *Furthermore, Moreover, Additionally, In conclusion, It is worth noting that* (tiếng Việt: *Hơn nữa, Thêm vào đó, Tóm lại là, Thiết nghĩ, Đáng chú ý là*). Thay thế bằng các từ nối tự nhiên hơn hoặc đi thẳng vào nội dung câu.
    *   *Hành văn chủ động (Active Voice):* Sử dụng ngôi thứ nhất số nhiều ("Chúng tôi tiến hành...") hoặc các câu khẳng định chủ động thay vì các câu bị động rườm rà.
    *   *Lồng ghép ngữ cảnh thực tế:* Đưa các tham số, lỗi cụ thể gặp phải trong quá trình debug thực tế vào bài viết để tạo độ tin cậy cao của con người.

---

## 3. Cấu Trúc Workspace Chuẩn
```
├── figures/              # Chứa toàn bộ hình ảnh, biểu đồ định dạng .png, .jpg
├── generate_huge_report.py  # File Python chứa mã nguồn LaTeX thô dưới dạng chuỗi r"""..."""
├── compile_report.py     # Script Python biên dịch tự động (quét lỗi gạch dưới, xóa cache, chạy XeLaTeX)
├── report.tex            # File nguồn LaTeX sạch (được sinh tự động từ compile_report.py)
├── report.pdf            # File báo cáo PDF đầu ra cuối cùng
├── report.aux # Lưu thông tin nhãn tham chiếu chéo
├── report.toc # Lưu cấu trúc mục lục
├── report.lof # Lưu danh mục hình ảnh
├── report.lot # Lưu danh mục bảng biểu
└── report.out # Lưu cấu trúc bookmark PDF
```

---

## 4. Mã Nguồn Script Biên Dịch Tự Động (`compile_report.py`)
Mọi dự án báo cáo LaTeX sau này cần sử dụng tệp `compile_report.py` có cấu trúc sau để thực hiện biên dịch tự động:

```python
# -*- coding: utf-8 -*-
import re
import os
import subprocess

# 1. Đọc mã nguồn LaTeX từ file generator
with open("generate_huge_report.py", "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'latex_code = r"""(.*?)"""', content, re.DOTALL)
if not match:
    print("Error: Could not find latex_code in generate_huge_report.py!")
    exit(1)

latex_body = match.group(1)

# 2. Hàm tự động quét và sửa lỗi gạch dưới (_)
def clean_latex(text):
    pattern = r'(\\begin\{(?:lstlisting|verbatim)\}.*?\\end\{(?:lstlisting|verbatim)\})'
    parts = re.split(pattern, text, flags=re.DOTALL)
    
    for i in range(len(parts)):
        if parts[i].startswith("\\begin{lstlisting}") or parts[i].startswith("\\begin{verbatim}"):
            continue
            
        cmd_pattern = r'(\\(?:label|ref|includegraphics|url)(?:\[[^\]]*\])?\{[^}]*\})'
        subparts = re.split(cmd_pattern, parts[i], flags=re.DOTALL)
        
        for j in range(len(subparts)):
            if (subparts[j].startswith("\\label") or 
                subparts[j].startswith("\\ref") or 
                subparts[j].startswith("\\includegraphics") or 
                subparts[j].startswith("\\url")):
                subparts[j] = subparts[j].replace("\\_", "_")
            else:
                subparts[j] = re.sub(r'(?<!\\)_', r'\\_', subparts[j])
                
        parts[i] = "".join(subparts)
        
    return "".join(parts)

cleaned_body = clean_latex(latex_body)

# 3. Ghi ra file report.tex
with open("report.tex", "w", encoding="utf-8") as f:
    f.write(cleaned_body)
print("SUCCESS: report.tex generated.")

# 4. Dọn dẹp cache phụ trợ (Được tắt đi mặc định để giữ lại cache giúp biên dịch cực nhanh)
# Chỉ khi nào bị lỗi tham chiếu chéo hoặc lỗi font nghiêm trọng thì mới cần xóa thủ công các file này.
# extensions = [".aux", ".toc", ".lof", ".lot", ".out", ".log"]
# for ext in extensions:
#     path = f"report{ext}"
#     if os.path.exists(path):
#         os.remove(path)
#         print(f"Deleted old {path}")

# Kiểm tra nếu đã có cache từ trước thì chỉ cần biên dịch 2 lần để tiết kiệm thời gian,
# nếu chưa có cache (lần chạy đầu tiên) thì biên dịch 3 lần.
has_cache = os.path.exists("report.aux")
passes = 2 if has_cache else 3

# 5. Biên dịch XeLaTeX để đồng bộ liên kết & số trang
for run in range(1, passes + 1):
    print(f"--- XeLaTeX Compile Pass {run}/{passes} ---")
    res = subprocess.run(["xelatex", "-interaction=nonstopmode", "report.tex"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error during Pass {run}!")
        print(res.stderr)
        if os.path.exists("report.log"):
            with open("report.log", "r", encoding="utf-8", errors="ignore") as log_f:
                lines = log_f.readlines()
                print("".join(lines[-30:]))
        exit(1)

print("SUCCESS: PDF compiled successfully.")
```

---

## 5. Hướng Dẫn Phối Hợp Tiết Kiệm Token & Tốc Độ Cao (User Collaboration Guide)

Để tối ưu hóa quá trình biên soạn, tránh lãng phí hạn ngạch (quota) của AI và tăng tốc độ xử lý, người dùng và AI hãy phối hợp theo 3 bước sau:

### Bước 1: Chuẩn bị hình ảnh trong `figures/` và file tóm tắt dữ liệu (`summary.md`)
*   **Phía người dùng:** Chạy code cục bộ để sinh ra toàn bộ hình ảnh đồ thị, lưu vào thư mục `figures/` và đặt tên rõ ràng (ví dụ: `lab1_fig1.png`). Gửi cho AI danh sách các tên file ảnh này kèm theo một file tóm tắt ngắn chứa số liệu chính để làm cơ sở dữ liệu gốc (Ground Truth).
*   **Phía AI (Bắt buộc):** Khi người dùng yêu cầu phân tích đồ thị, AI phải gọi công cụ `view_file` để tự xem ảnh trực tiếp. AI không được viết phỏng đoán hoặc bịa số liệu dựa trên lý thuyết chung chung (tránh ảo giác) nhằm đảm bảo bài viết có chiều sâu học thuật chân thực nhất.

### Bước 2: Tự chạy biên dịch cục bộ (Local Compile & Shortcut Scripts)
Chạy trực tiếp file script biên dịch trên máy tính cá nhân của bạn (hoàn toàn miễn phí, không tốn quota AI). Bạn có thể sử dụng các file kịch bản chạy nhanh (shortcut) để nhấp đúp chuột biên dịch nhanh tùy theo hệ điều hành:

*   **Trên Windows (Sử dụng file `.bat`):**
    Tạo một file tên là `run.bat` cùng cấp thư mục dự án với nội dung sau:
    ```batch
    @echo off
    python compile_report.py
    start report.pdf
    ```
    *Cách dùng:* Chỉ cần **click đúp chuột** trực tiếp vào file `run.bat`, hệ thống sẽ tự động chạy biên dịch và mở file PDF kết quả lên màn hình.

*   **Trên macOS / Linux (Sử dụng file `.sh`):**
    Tạo một file tên là `run.sh` cùng cấp thư mục dự án với nội dung sau:
    ```bash
    #!/bin/bash
    python3 compile_report.py
    open report.pdf
    ```
    *Cách dùng:* Mở terminal tại thư mục dự án, chạy lệnh cấp quyền chạy `chmod +x run.sh` (chỉ chạy một lần đầu), sau đó mỗi lần cần dịch chỉ cần gõ `./run.sh` để biên dịch và tự động hiển thị PDF.

### Bước 3: Gửi log lỗi cực ngắn khi gặp sự cố
Nếu biên dịch bị lỗi (màn hình hiển thị chữ đỏ hoặc dừng giữa chừng), bạn không cần gửi cả file log lớn cho AI.
*   Hãy mở file `report.log` hoặc nhìn trực tiếp trên màn hình terminal.
*   Tìm dòng có dấu chấm than **`!`** ở đầu dòng (đây là dòng chỉ ra nguyên nhân lỗi cụ thể).
*   Copy duy nhất dòng đó gửi cho AI (ví dụ: `! LaTeX Error: File figures/hinh_anh_1.png not found.`).

---

## 6. Phạm Vi Áp Dụng Cho Các Nhóm Ngành Học

Quy chuẩn này được thiết kế linh hoạt để áp dụng hiệu quả cho cả hai nhóm ngành lớn:

### 6.1. Nhóm ngành Khoa học Tự nhiên, Toán Tin, Kỹ thuật (STEM)
*   **Yêu cầu cốt lõi:** Tập trung vào thuật toán, công thức toán học, bảng số liệu thực nghiệm và code lập trình.
*   **Các lệnh & Môi trường LaTeX chủ đạo AI cần dùng:**
    *   Sử dụng `$ ... $` cho ký hiệu toán nội dòng (inline) và `\[ ... \]` hoặc `equation` cho các phương trình lớn xếp dòng riêng biệt.
    *   Sử dụng môi trường `\begin{lstlisting} ... \end{lstlisting}` (gói `listings`) để hiển thị mã nguồn code rõ ràng.
    *   Sử dụng `figure` kết hợp gói `float` (lệnh `[H]`) để cố định hình ảnh đồ thị ngay sau đoạn văn giải thích.
    *   Sử dụng `\resizebox` cho bảng biểu số liệu lớn để chống tràn lề trang.

### 6.2. Nhóm ngành Khoa học Xã hội, Lý luận Chính trị, Nhân văn
*   **Yêu cầu cốt lõi:** Tập trung vào cấu trúc lập luận logic chặt chẽ, đoạn văn mạch lạc, trích dẫn tài liệu tham khảo chính xác và các phân cấp danh sách rõ ràng.
*   **Các lệnh & Môi trường LaTeX chủ đạo AI cần dùng:**
    *   Sử dụng môi trường `\begin{quote} ... \end{quote}` khi trích dẫn các đoạn văn kiện Đảng, danh ngôn, nghị quyết, điều luật hoặc nhận định của các tác giả lớn.
    *   Sử dụng chú thích chân trang `\footnote{...}` để giải thích thêm ngữ cảnh lịch sử hoặc các từ ngữ chuyên ngành ở dưới chân trang mà không làm loãng mạch văn nghị luận chính.
    *   Sử dụng danh sách phân cấp nhiều tầng (`itemize` cho dấu chấm tròn, `enumerate` cho số thứ tự) để trình bày giải pháp hoặc nguyên tắc lý luận.
    *   Quản lý và định dạng tài liệu tham khảo chuẩn chỉnh cuối bài theo các hệ thống chuẩn xã hội (ví dụ: APA/Harvard).


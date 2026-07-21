# -*- coding: utf-8 -*-
import re
import os
import subprocess

# 1. Read generate_huge_report.py
with open("generate_huge_report.py", "r", encoding="utf-8") as f:
    content = f.read()

# Extract the raw latex_code string
match = re.search(r'latex_code = r"""(.*?)"""', content, re.DOTALL)
if not match:
    print("Error: Could not find latex_code in generate_huge_report.py!")
    exit(1)

latex_body = match.group(1)

# 2. Clean underscores function
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

# 3. Write report.tex
with open("report.tex", "w", encoding="utf-8") as f:
    f.write(cleaned_body)
print("SUCCESS: report.tex generated.")

# 4. Clean auxiliary files
extensions = [".aux", ".toc", ".lof", ".lot", ".out", ".log"]
for ext in extensions:
    path = f"report{ext}"
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted old {path}")

# 5. Compile with xelatex three times
for run in range(1, 4):
    print(f"--- XeLaTeX Compile Pass {run}/3 ---")
    res = subprocess.run(["xelatex", "-interaction=nonstopmode", "report.tex"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error during Pass {run}!")
        print(res.stderr)
        # Print the last few lines of log to debug
        if os.path.exists("report.log"):
            with open("report.log", "r", encoding="utf-8", errors="ignore") as log_f:
                lines = log_f.readlines()
                print("".join(lines[-30:]))
        exit(1)

print("SUCCESS: PDF compiled successfully.")

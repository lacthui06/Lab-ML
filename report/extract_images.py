# -*- coding: utf-8 -*-
import os
import json
import base64

# Define notebook paths
notebooks = {
    # Lab 1
    "lab1_eda": r"lab1/eda/eda.ipynb",
    "lab1_feature": r"lab1/feature egineer/feature_engineering.ipynb",
    "lab1_modeling": r"lab1/modeling/logistic.ipynb",
    # Lab 2
    "lab2_eda": r"lab2/eda/eda.ipynb",
    "lab2_feature": r"lab2/feature_engineer/feature_engineering.ipynb",
    "lab2_modeling": r"lab2/modeling/modeling.ipynb",
    # Lab 3
    "lab3_eda": r"lab3/eda/eda.ipynb",
    "lab3_feature": r"lab3/feature_engineer/feature_engineer.ipynb",
    "lab3_modeling": r"lab3/modeling/modeling.ipynb",
    "lab3_image": r"lab3/additional/image_segmentation.ipynb",
    # Lab 4
    "lab4_eda": r"lab4/eda/eda.ipynb",
    "lab4_feature": r"lab4/feature egineer/feature_engineering.ipynb",
    "lab4_modeling": r"lab4/modeling/modeling_kaggle.ipynb"
}

output_dir = r"figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Starting image extraction from notebooks...")

for key, rel_path in notebooks.items():
    abs_path = os.path.abspath(rel_path)
    if not os.path.exists(abs_path):
        print(f"File not found: {abs_path}")
        continue
    
    print(f"Reading {key} from {rel_path}...")
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Error reading JSON from {rel_path}: {e}")
        continue
        
    img_counter = 1
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        
        # Check outputs
        for output in cell.get('outputs', []):
            data = output.get('data', {})
            # Look for image/png in outputs
            if 'image/png' in data:
                b64_data = data['image/png'].replace('\n', '')
                filename = f"{key}_fig{img_counter}.png"
                dest_path = os.path.join(output_dir, filename)
                
                try:
                    with open(dest_path, 'wb') as img_f:
                        img_f.write(base64.b64decode(b64_data))
                    print(f"  Extracted: {filename}")
                    img_counter += 1
                except Exception as e:
                    print(f"  Error decoding image in {key}: {e}")

print("Image extraction completed. All extracted images are in the 'figures' folder.")

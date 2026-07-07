# Walkthrough - California Housing Price Prediction (All PAs Benchmarking)

We have successfully executed the end-to-end training pipeline on the **California Housing dataset** across the **4 newly refactored Feature Engineering scenarios**:

- **PA1 (Base Features)**: Original features (longitude, latitude, age, and log-transformed variables).
- **PA2 (Reduced)**: Latitude/longitude replaced by `coords_sum`. Dropped total_bedrooms and households.
- **PA3_A (Mean Aggregation)**: Geograpy goped via `coords_sum`. Collinear features goped via arithmetic mean.
- **PA3_B (PCA Aggregation)**: Geograpy goped via `coords_sum`. Collinear features goped via PCA 1D (`size_pc1`).

---

## 1. Experimental Results (All PAs Comparison)

Below is the comparative performance table on the test set:

| Scenario | Model | MAE (USD) | RMSE (USD) | MAPE (%) | $R^2$ Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **PA1 (Base Features)** | **PyTorch MLP** | **33,801** | **50,716** | **18.94** | **0.8037** 🏆 *(Best)* |
| (13 columns) | Random Forest Scratch | 42,254 | 59,673 | 24.42 | 0.7283 |
| | Linear Regression | 54,395 | 72,989 | 32.22 | 0.5935 |
| **PA2 (Reduced)** | PyTorch MLP | 38,826 | 56,709 | 22.22 | 0.7546 |
| (10 columns) | Random Forest Scratch | 43,562 | 62,420 | 25.09 | 0.7027 |
| | Linear Regression | 55,361 | 73,754 | 32.68 | 0.5849 |
| **PA3_A (Mean)** | PyTorch MLP | 39,678 | 57,943 | 22.52 | 0.7438 |
| (10 columns) | Random Forest Scratch | 44,659 | 63,596 | 25.62 | 0.6914 |
| | Linear Regression | 55,891 | 74,637 | 32.79 | 0.5749 |
| **PA3_B (PCA)** | PyTorch MLP | 43,866 | 63,392 | 24.63 | 0.6933 |
| (9 columns) | Random Forest Scratch | 46,290 | 64,955 | 26.79 | 0.6780 |
| | Linear Regression | 57,337 | 76,555 | 33.35 | 0.5528 |

---

## 2. Deep-Dive Findings

1. **PA1 (Base Features) is the absolute winner**:
   - **PyTorch MLP** achieves a peak **$R^2$ of 0.8037** and a very low **MAPE of 18.94%**.
   - Keeping `longitude` and `latitude` separate is essential for deep neural networks to approximate the complex geographical boundary price variations of California.
2. **Impact of Coordinate Goping**:
   - Replacing coordinates with `coords_sum` decreases accuracy in all models. The drop is most severe for PyTorch MLP (dropping from 0.8037 down to 0.7546 in PA2).
3. **PCA vs. Mean Aggregation (PA3_B vs. PA3_A)**:
   - Arithmetic mean aggregation (**PA3_A**) preserves predictive power slightly better than PCA 1D aggregation (**PA3_B**) on this dataset (R² is ~0.74 vs. ~0.69 for MLP). 
   - PCA 1D compresses too much detailed variance into a single dimension, losing important local block size information.

---

## 3. Kaggle Deployment & GPU Acceleration

- **GPU Acceleration**: We updated the `train_mlp` function to run 100% on GPU (device = CUDA). Both local and Kaggle versions now push model parameters, mini-batches, and validation datasets to the GPU to speed up training.
- **GPU Check**: Added an automatic GPU check block at the top of `modeling_kaggle.ipynb` to verify PyTorch CUDA availability and print device information (e.g. Tesla T4).
- **Clean Workspace**: All local temporary CSV subdirectories and files have been cleaned up. The raw data can be recreated anytime by executing the feature engineering pipeline.

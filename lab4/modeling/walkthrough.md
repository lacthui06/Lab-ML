# Walkthrough - California Housing Price Prediction

This document records the final implementation, optimizations, and results for the `modeling.ipynb` benchmarking on the California Housing dataset.

---

## 1. Accomplished Work

### Target Preprocessing & Model Training
- **Target Value Processing**: Standardized `median_house_value` using `StandardScaler` directly (without log-transforming). This successfully solved convergence oscillations in SVR/Linear Regression Scratch models.
- **Model Implementations**: Benchmarked Linear Regression Scratch (Gradient Descent), SVR Scratch (Subgradient Descent), and PyTorch MLP (Adam with Plateau Scheduler).
- **GPU compatibility**: Handled device configurations (`.to(device)` and `.cpu().numpy()`) to allow the notebook to run seamlessly on CPU or GPU (such as Google Colab / Kaggle).

### Optuna Hyperparameter Optimization
- Replaced traditional Grid Search with **Optuna** (Bayesian Optimization) to tune SVR, Linear Regression, and MLP hyper-parameters.
- Fixed Optuna syntax bugs (swapped low/high order parameters, and used `suggest_categorical` for discrete value lists).
- Configured 10 trials per model, using fewer epochs (30 epochs) during MLP tuning trials for speed, and 100 epochs for the final scenario runs to ensure optimal convergence.

### Output Visualizations & Formatting
- **Learning Curves**: Plotted convergence histories for all models in the Full Features scenario. Added print logging to the PyTorch training loop to print loss and $R^2$ after each epoch.
- **Bar Charts**: Plotted comparison charts for MAE, RMSE, MAPE, and $R^2$ across models and scenarios.
- **Scatter Matrix (3x3)**: Plotted actual vs. predicted values for all models across all 3 scenarios.
- **Formatted Axes**: Fixed y-axis labels on the bar charts and scatter plots to display regular numbers (with thousands separators, e.g. `500,000` USD) instead of scientific notation (`1e6`).
- **Plot Limits**: Clipped prediction scatter axes to the realistic range `[0, 550,000]` USD, preventing a few outlier SVR predictions from compressing the chart and allowing the visual points to spread out nicely.

---

## 2. Final Benchmarking Results

Below is the summary table of the final Optuna-tuned models on the California Housing test split (Full Features scenario has 22 columns since the missingness indicator column was removed):

| Scenario | Model | MAE (USD) | RMSE (USD) | MAPE (%) | $R^2$ Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Full Features** | **PyTorch MLP** | **34,408** | **52,315** | **19.14** | **0.7911** *(Best)* |
| (22 columns) | Linear Regression | 50,166 | 71,197 | 29.98 | 0.6132 |
| | SVR (Scratch) | 49,676 | 73,050 | 28.05 | 0.5928 |
| **PCA Features** | **PyTorch MLP** | 44,480 | 67,638 | 22.39 | **0.6509** |
| (13 columns) | Linear Regression | 55,462 | 80,186 | 33.17 | 0.5093 |
| | SVR (Scratch) | 53,091 | 79,615 | 30.17 | 0.5163 |
| **Mutual Info Features**| **PyTorch MLP** | 36,039 | 54,338 | 20.51 | **0.7747** |
| (Top 10 selected) | Linear Regression | 53,959 | 77,447 | 30.92 | 0.5423 |
| | SVR (Scratch) | 51,670 | 77,552 | 27.69 | 0.5410 |

### Key Takeaways:
- **Optimization Success**: SVR Scratch and Linear Regression Scratch achieve strong positive $R^2$ scores (~0.59 and ~0.61 respectively) and stable convergence.
- **MLP Performance**: PyTorch MLP achieves the highest accuracy overall with $R^2 = 0.7911$ and MAE = 34,408 USD on Full Features.

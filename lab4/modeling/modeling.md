# Modeling Plan - California Housing Price Prediction

This document records the planned architecture, methodology, and benchmarking setup for `modeling.ipynb` and `modeling_kaggle.ipynb`.

## 1. Goal & Objectives
The goal is to implement, optimize, and compare three regression models on the California Housing dataset to predict house prices (`median_house_value`) across four distinct feature scenarios (PA1, PA2, PA3_A, PA3_B).

## 2. Target Variable Preprocessing
- **No Log Transform**: The target variable `median_house_value` is processed using standard scaling only (`StandardScaler`) to preserve the raw linear relationships and prevent subgradient descent oscillations.
- **Inverse Transformation**: All predictions are back-transformed to the original USD scale (`scaler_y.inverse_transform`) to calculate metrics.

## 3. Models to Benchmark
1. **Linear Regression from Scratch** (Gradient Descent optimization).
2. **Random Forest Regressor from Scratch** (Ensemble of Decision Tree Regressors optimized with percentile splits to speed up training).
3. **PyTorch MLP (Multilayer Perceptron)** (Deep neural network using batch normalization, dropout, Adam optimizer, and learning rate scheduling).

## 4. Feature Scenario Matrix
Models are trained and evaluated under four feature engineering scenarios:
- **PA1 (Base Features)**: 13 columns. Original numerical features (with log transforms) and One-Hot encoded categoricals.
- **PA2 (Reduced)**: 10 columns. Dropped Bedrooms and Households; longitude and latitude combined into `coords_sum`.
- **PA3_A (Mean Aggregation)**: 10 columns. Longitude/latitude combined into `coords_sum`; collinear pairs combined via arithmetic mean.
- **PA3_B (PCA Aggregation)**: 9 columns. Longitude/latitude combined into `coords_sum`; all 4 collinear size features combined into 1D PCA component (`size_pc1`).

## 5. Hyperparameter Optimization (Optuna)
Instead of Grid Search, **Optuna** (Bayesian Optimization) is used to tune:
- **Linear Regression**: `lr` (log-uniform) and `epochs`.
- **Random Forest Scratch**: `n_estimators`, `max_depth`, and `min_samples_split`.
- **PyTorch MLP**: `lr` (log-uniform), `batch` size, and `wd` (weight decay).

## 6. GPU Detection & Acceleration
- **NumPy Models**: Linear Regression and Random Forest Scratch models are trained on the **CPU**.
- **PyTorch MLP**: Fully accelerated on the **GPU** (CUDA) if available. The model, batch loader, and validation tensors are pushed to `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`.
- **GPU Check**: Added a GPU print check block at the top of the notebooks to verify PyTorch CUDA availability and device name (e.g. Tesla T4).

## 7. Evaluation & Visualizations Planned
- **Metrics**: MAE (USD), RMSE (USD), MAPE (%), $R^2$ Score, Train Time (ms), and Inference Time (ms).
- **Learning Curves**: Dynamic plotting of Loss histories for all three models on the **best-performing scenario** overall.
- **Metrics Bar Charts**: Comparison of MAE, RMSE, MAPE, and $R^2$ across models and all 4 scenarios.
- **Prediction Scatter Matrix (3x4)**: Plots of Actual vs. Predicted values for all 3 models across all 4 scenarios. Axes are formatted to show standard numbers (with commas, no scientific notation) and limited to `[0, 550,000]` USD.

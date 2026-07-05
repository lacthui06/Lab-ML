# Modeling Plan - California Housing Price Prediction

This document records the planned architecture, methodology, and benchmarking setup for `modeling.ipynb`.

## 1. Goal & Objectives
The goal is to implement, optimize, and compare three regression models on the California Housing dataset to predict house prices (`median_house_value`) across three distinct feature representations.

## 2. Target Variable Preprocessing
- **No Log Transform**: The target variable `median_house_value` is processed using standard scaling only (`StandardScaler`) to preserve the raw linear relationships and prevent subgradient descent oscillations.
- **Inverse Transformation**: All predictions are back-transformed to the original USD scale (`scaler_y.inverse_transform`) to calculate metrics.

## 3. Models to Benchmark
1. **Linear Regression from Scratch** (Gradient Descent optimization).
2. **SVR (Support Vector Regression) from Scratch** (Subgradient Descent with $\epsilon$-insensitive loss and L2 regularization).
3. **PyTorch MLP (Multilayer Perceptron)** (Deep neural network using Adam optimizer and learning rate scheduling).

## 4. Feature Scenario Matrix
Models are trained and evaluated under three scenarios:
- **Full Features**: All 22 engineered features.
- **PCA Features**: 13 principal components capturing 95% variance.
- **Mutual Information Features**: Top 10 features selected via Mutual Information regression.

## 5. Hyperparameter Optimization (Optuna)
Instead of Grid Search, **Optuna** (Bayesian Optimization) is used to tune:
- **Linear Regression**: `lr` (log-uniform) and `epochs`.
- **SVR Scratch**: `lr` (log-uniform), `epochs`, `C`, `epsilon`, and `reg` (L2 strength).
- **PyTorch MLP**: `lr` (log-uniform), `batch` size, and `wd` (weight decay).

## 6. Evaluation & Visualizations Planned
- **Metrics**: MAE (USD), RMSE (USD), MAPE (%), $R^2$ Score, Train Time (ms), and Inference Time (ms).
- **Learning Curves**: Loss histories for all three models to track convergence.
- **Metrics Bar Charts**: Comparison of MAE, RMSE, MAPE, and $R^2$ across models and scenarios.
- **Prediction Scatter Matrix (3x3)**: Plots of Actual vs. Predicted values. Axes are formatted to show standard numbers (with commas, no scientific notation) and limited to `[0, 550,000]` USD to focus on core data.

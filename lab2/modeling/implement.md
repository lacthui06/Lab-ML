# MODELING
**SVM Regressor From Scratch**
class SVM():
    def __init__(self, lr = 0.001, lamda = 0.01, n_iters = 1000):
        self.lr = lr
        self.lamda = lamda
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_sample, n_feature = X.shape 
        self.w = np.zeros(n_feature)
        self.b = 0

        for _ in range (self.n_iters):
            for i, x_i in enumerate(X):
                if y[i] * (x_i @ self.w + self.b) >= 1:
                    self.w -= self.lr * (2 * self.lamda * self.w)
                else:
                    self.w -= self.lr * (2 * self.lamda * self.w - y[i] * x_i)
                    self.b -= self.lr * y[i]

    def predict(self, X):
        return np.sign(X @ self.w + self.b)
* Train in kết quả - visualize sau đó hyper param lấy kết quả so sánh khi chưa tunning.

**Experiment with different param and evaluation the result using appropriate metrics**

# EVALUATION
**Evaluate the model's performance on the testing set using metrics like R^2, MSE, MAE, MAPE or RMSE. Visualize with dataset**
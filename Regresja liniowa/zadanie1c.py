#!/usr/bin/env python3

import numpy as np
import pytest
from sklearn.linear_model import Ridge

class RidgeRegr:
    
    def __init__(self, alpha=0, learning_rate=0.01, tolerance=1e-8, max=1e6):
        
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.tolerance = tolerance
        self.max = max

    def fit(self, X, Y):
        # wejscie:
        #  X = np.array, shape = (n, m)
        #  Y = np.array, shape = (n)
        # Znajduje theta (w przyblizeniu) minimalizujace kwadratowa funkcje kosztu L uzywajac metody iteracyjnej.
        
        n, m = X.shape
        X = np.hstack((np.array([1]*n).reshape((n, 1)), X))     #dodajemy 1

        self.theta = np.zeros((m+1))
        theta = self.theta

        iteracje = 0
        while iteracje < self.max:
            

            self.theta = self.theta - self.learning_rate * (X.T @ (X @ self.theta - Y) + self.alpha * np.concatenate(([0], self.theta[1:])))
            
            if np.linalg.norm(self.theta-theta) < self.tolerance: return self

            theta = self.theta
            iteracje += 1
        
        print(f"Przekroczono maksymalną liczbę iteracji: {self.max}")
        return self
    
    def predict(self, X):
        
        # wejscie
        #  X = np.array, shape = (k, m)
        # zwraca
        #  Y = wektor(f(X_1), ..., f(X_k))
        
        k, m = X.shape
        ans = np.hstack((np.array([1]*k).reshape((k, 1)), X)) @ self.theta
        return ans


def test_RidgeRegressionInOneDim():
    X = np.array([1, 3, 2, 5]).reshape((4, 1))
    Y = np.array([2, 5, 3, 8])
    X_test = np.array([1, 2, 10]).reshape((3, 1))
    alpha = 0.3
    expected = Ridge(alpha).fit(X, Y).predict(X_test)
    actual = RidgeRegr(alpha).fit(X, Y).predict(X_test)
    assert list(actual) == pytest.approx(list(expected), rel=1e-5)

def test_RidgeRegressionInThreeDim():
    X = np.array([1, 2, 3, 5, 4, 5, 4, 3, 3, 3, 2, 5]).reshape((4, 3))
    Y = np.array([2, 5, 3, 8])
    X_test = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 5, 7, -2, 0, 3]).reshape((5, 3))
    alpha = 0.4
    expected = Ridge(alpha).fit(X, Y).predict(X_test)
    actual = RidgeRegr(alpha).fit(X, Y).predict(X_test)
    assert list(actual) == pytest.approx(list(expected), rel=1e-3)

test_RidgeRegressionInOneDim()
test_RidgeRegressionInThreeDim()
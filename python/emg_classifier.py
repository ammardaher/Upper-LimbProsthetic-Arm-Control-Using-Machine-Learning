"""
EMG Signal Classification Module
Handles Decision Tree classifier for EMG signal classification
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib
from typing import Tuple, Optional


class EMGClassifier:
    """
    Decision Tree classifier for EMG signal classification.
    Classifies 4 pinch movements from EMG signals.
    """
    
    def __init__(self, max_depth: int = 32):
        """
        Initialize the EMG classifier.
        
        Args:
            max_depth: Maximum depth of the decision tree (default: 32)
        """
        self.classifier = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        self.is_trained = False
        self.classes = {
            0: "Pinch1",  # Thumb + Index
            1: "Pinch2",  # Thumb + Middle
            2: "Pinch3",  # Thumb + Ring
            3: "Pinch4"   # Thumb + Pinky
        }
    
    def train(self, X: np.ndarray, y: np.ndarray) -> dict:
        """
        Train the classifier on provided data.
        
        Args:
            X: Feature matrix of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
        
        Returns:
            Dictionary with training metrics (accuracy, feature_importance)
        """
        self.classifier.fit(X, y)
        self.is_trained = True
        
        # Calculate training accuracy
        train_accuracy = self.classifier.score(X, y)
        
        return {
            "accuracy": train_accuracy,
            "n_samples": X.shape[0],
            "n_features": X.shape[1],
            "classes": len(np.unique(y))
        }
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for samples.
        
        Args:
            X: Feature matrix of shape (n_samples, n_features)
        
        Returns:
            Predicted class labels
        """
        if not self.is_trained:
            raise ValueError("Classifier must be trained before prediction")
        
        return self.classifier.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities.
        
        Args:
            X: Feature matrix of shape (n_samples, n_features)
        
        Returns:
            Probability estimates for each class
        """
        if not self.is_trained:
            raise ValueError("Classifier must be trained before prediction")
        
        return self.classifier.predict_proba(X)
    
    def get_confidence(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get predictions with confidence scores.
        
        Args:
            X: Feature matrix
        
        Returns:
            Tuple of (predictions, confidence_scores)
        """
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        confidences = np.max(probabilities, axis=1)
        
        return predictions, confidences
    
    def save_model(self, filepath: str) -> None:
        """
        Save trained model to disk.
        
        Args:
            filepath: Path to save the model (.pkl format)
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        joblib.dump(self.classifier, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """
        Load trained model from disk.
        
        Args:
            filepath: Path to the saved model file
        """
        self.classifier = joblib.load(filepath)
        self.is_trained = True
        print(f"Model loaded from {filepath}")
    
    def get_feature_importance(self) -> dict:
        """
        Get feature importance scores.
        
        Returns:
            Dictionary mapping feature index to importance score
        """
        if not self.is_trained:
            raise ValueError("Classifier must be trained first")
        
        importances = self.classifier.feature_importances_
        return {f"Feature_{i}": imp for i, imp in enumerate(importances)}
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """
        Evaluate classifier on test data.
        
        Args:
            X_test: Test feature matrix
            y_test: True test labels
        
        Returns:
            Dictionary with evaluation metrics
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        predictions = self.predict(X_test)
        
        return {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average='weighted'),
            "recall": recall_score(y_test, predictions, average='weighted'),
            "f1_score": f1_score(y_test, predictions, average='weighted'),
            "n_test_samples": X_test.shape[0]
        }


if __name__ == "__main__":
    # Example usage
    print("EMG Classifier Module")
    print("Import this module to use the EMGClassifier class")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

# Create directories if they don't exist
os.makedirs('models', exist_ok=True)
os.makedirs('reports', exist_ok=True)

def run_milestone_1():
    print("--- Milestone 1: Data Preparation & CART Modeling ---")
    
    # 1. Load Data
    df = pd.read_csv('data/Dataset2.csv')
    print(f"Dataset loaded: {len(df)} records.")

    # 2. Exploratory Data Analysis (EDA)
    print("\n[EDA] Checking correlations...")
    # Select numeric columns for correlation
    numeric_cols = ['Skor_Komunikasi', 'Skor_Laporan', 'Skor_Rapat', 'Skor_Partisipasi']
    corr = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='RdYlGn', fmt=".2f")
    plt.title('Correlation Heatmap of Stakeholder Scores')
    plt.savefig('reports/eda_correlation.png')
    print("EDA Correlation plot saved to reports/eda_correlation.png")

    # 3. Preprocessing
    X = df[numeric_cols]
    y = df['Label_Akhir']
    
    # Label Encoding for target
    # Harmonis -> 1, Kurang Harmonis -> 0
    y_encoded = y.map({'Harmonis': 1, 'Kurang Harmonis': 0})
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    print(f"Data split: {len(X_train)} training, {len(X_test)} testing.")

    # 4. CART Modeling (Decision Tree)
    print("\n[Modeling] Training Decision Tree (CART)...")
    model = DecisionTreeClassifier(
        criterion='gini',      # Standard CART
        max_depth=5,           # Prevent overfitting
        min_samples_split=5,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # 5. Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Kurang Harmonis', 'Harmonis']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Kurang Harmonis', 'Harmonis'],
                yticklabels=['Kurang Harmonis', 'Harmonis'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig('reports/confusion_matrix.png')
    
    # Cross Validation
    cv_scores = cross_val_score(model, X, y_encoded, cv=5)
    print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # 6. Tree Visualization
    plt.figure(figsize=(20, 10))
    plot_tree(model, feature_names=numeric_cols, class_names=['Kurang Harmonis', 'Harmonis'], filled=True, rounded=True)
    plt.savefig('reports/decision_tree_visual.png')
    print("Tree visualization saved to reports/decision_tree_visual.png")

    # 7. Export Model
    joblib.dump(model, 'models/stakeholder_cart_model.joblib')
    # Save the mapping as well
    joblib.dump({'Harmonis': 1, 'Kurang Harmonis': 0}, 'models/label_mapping.joblib')
    print("\nModel and mapping exported to models/ directory.")
    
    print("\n--- Milestone 1 Completed Successfully ---")

if __name__ == "__main__":
    run_milestone_1()

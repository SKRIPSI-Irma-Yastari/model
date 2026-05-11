import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train():
    # 1. Load Data
    data_path = 'data/Dataset_Monitoring_BPMA_Interaksi_Lengkap.csv'
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    
    # 2. Preprocessing
    # Features to use: Nama KKKS, Jenis Interaksi, Skor
    # We'll need to encode categorical data
    
    # Initialize encoders
    le_kkks = LabelEncoder()
    le_interaksi = LabelEncoder()
    le_label = LabelEncoder()
    
    df['Nama KKKS_Encoded'] = le_kkks.fit_transform(df['Nama KKKS'])
    df['Jenis Interaksi_Encoded'] = le_interaksi.fit_transform(df['Jenis Interaksi'])
    df['Label_Encoded'] = le_label.fit_transform(df['Label'])
    
    # Features and Target
    X = df[['Nama KKKS_Encoded', 'Jenis Interaksi_Encoded', 'Skor']]
    y = df['Label_Encoded']
    
    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Decision Tree
    model = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le_label.classes_))
    
    # 6. Export Model and Encoders
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/decision_tree_model.joblib')
    joblib.dump(le_kkks, 'models/le_kkks.joblib')
    joblib.dump(le_interaksi, 'models/le_interaksi.joblib')
    joblib.dump(le_label, 'models/le_label.joblib')
    print("Model and encoders exported to 'models/' directory.")

if __name__ == "__main__":
    train()

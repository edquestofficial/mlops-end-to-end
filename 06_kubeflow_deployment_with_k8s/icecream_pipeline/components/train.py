import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def train(input_csv_path: str, model_path: str):

    df = pd.read_csv(input_csv_path)
    X = df[['temp']]
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

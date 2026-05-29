from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd

def train_model(df):

    # clean
    df = df.dropna(subset=[
        'product_category_name',
        'price',
        'freight_value'
    ])

    # features
    X_num = df[['price', 'freight_value']]
    X_cat = pd.get_dummies(df['product_category_name'])
    X = pd.concat([X_num, X_cat], axis=1)

    # target
    y = df['is_return'].astype(int)

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # model
    model = LogisticRegression(max_iter=1000, n_jobs=-1)
    model.fit(X_train, y_train)

    # predictions
    y_pred = model.predict(X_test)

    # metrics
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return model, X.columns, accuracy, cm, report
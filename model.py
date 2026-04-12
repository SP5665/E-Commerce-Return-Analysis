import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_model(df):
    df = df.dropna(subset=['product_category_name', 'price', 'freight_value']) #freight = shipping cost

    # numeric features
    X_num = df[['price', 'freight_value']]

    # categorical encoding
    X_cat = pd.get_dummies(df['product_category_name'])

    # combine
    X = pd.concat([X_num, X_cat], axis=1)

    y = df['is_return'].astype(int)

    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X, y)

    return model, X.columns
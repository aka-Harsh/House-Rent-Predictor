import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

def load_data():
    return pd.read_csv('Metro_House_Rent.csv')

def preprocess_data(df):
    le_city = LabelEncoder()
    le_area = LabelEncoder()
    df['city_encoded'] = le_city.fit_transform(df['city'])
    df['area_encoded'] = le_area.fit_transform(df['area'])

    df = df.dropna(subset=['city', 'area', 'rooms', 'bathroom', 'total_rent'])

    X = df[['city_encoded', 'area_encoded', 'rooms', 'bathroom']]
    y = df['total_rent']

    imputer = SimpleImputer(strategy='median')
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

    return X, y, le_city, le_area

def train_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_rent(model, le_city, le_area, city, area, rooms, bathrooms):
    city_encoded = le_city.transform([city])[0]
    area_encoded = le_area.transform([area])[0]
    input_data = np.array([[city_encoded, area_encoded, rooms, bathrooms]])
    return model.predict(input_data)[0]

def get_recommendations(df, city, rooms, bathrooms, budget):
    df_filtered = df[df['city'] == city]
    df_filtered['score'] = abs(df_filtered['rooms'] - rooms) + abs(df_filtered['bathroom'] - bathrooms)
    df_filtered = df_filtered.sort_values('score')

    if budget != 'Above 50000':
        min_budget, max_budget = map(int, budget.replace('Below ', '').split('-'))
        df_filtered = df_filtered[(df_filtered['total_rent'] >= min_budget) & (df_filtered['total_rent'] <= max_budget)]
    else:
        df_filtered = df_filtered[df_filtered['total_rent'] > 50000]

    recommendations = df_filtered.head().to_dict('records')
    return recommendations
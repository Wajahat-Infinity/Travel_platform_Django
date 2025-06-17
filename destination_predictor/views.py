from django.shortcuts import render
import os
import joblib
import pandas as pd
import numpy as np

# Load model and preprocessors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'model_files/destination_clustering_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'model_files/destination_scaler.pkl'))
label_encoders = joblib.load(os.path.join(BASE_DIR, 'model_files/destination_label_encoders.pkl'))

# Load original training dataset with clusters
data_path = os.path.join(BASE_DIR, 'model_files/data.xlsx')
df_full = pd.read_excel(data_path)

def predict_destination(request):
    prediction = None
    recommended_destinations = []

    if request.method == 'POST':
        input_data = {
            'Interest': request.POST.get('Interest'),
            'Goal of Travel': request.POST.get('Goal'),
            'Climate': request.POST.get('Climate'),
            'Solo/Group': request.POST.get('SoloGroup'),
            'Access': request.POST.get('Access'),
            'Distance from Capital (Islamabad) (km)': float(request.POST.get('Distance')),
            'Latitude': float(request.POST.get('Latitude')),
            'Longitude': float(request.POST.get('Longitude')),
            'Activity': request.POST.get('Activity'),
        }

        df_input = pd.DataFrame([input_data])

        # Encode categorical
        for col, le in label_encoders.items():
            df_input[col] = le.transform(df_input[col])

        # Scale input
        X_scaled = scaler.transform(df_input)

        # Predict cluster
        cluster = int(model.predict(X_scaled)[0])
        prediction = f"Predicted Cluster: {cluster}"

        # Find similar destinations in the same cluster
        similar = df_full[df_full['Cluster'] == cluster].copy()

        # Match columns used in training
        features = df_input.columns
        similar_scaled = scaler.transform(similar[features])
        distance = np.linalg.norm(similar_scaled - X_scaled, axis=1)

        similar['Distance'] = distance
        top_5 = similar.sort_values('Distance').head(5)
        recommended_destinations = top_5['Destination'].tolist()

    return render(request, 'destination_predictor/predict.html', {
        'prediction': prediction,
        'recommendations': recommended_destinations
    })

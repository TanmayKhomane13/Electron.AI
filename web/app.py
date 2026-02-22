from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import numpy as np
import os
from datetime import datetime
import requests
import json

# -----------------------------------
# Flask Setup
# -----------------------------------

app = Flask(__name__, static_folder="static")
CORS(app)

# -----------------------------------
# Load Electricity Model
# -----------------------------------

MODEL_PATH = "ml_models/demand_load_model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model_data = pickle.load(f)



    print("✅ Electricity Load Model loaded successfully!")



except Exception as e:
    print(f"❌ Model load failed: {e}")
    exit(1)



# Transformer-specific coordinates (hyper-local weather!)
TRANSFORMER_COORDS = {
    "T1-Bandra": (19.0671, 72.8657),
    "T2-Dadar": (19.0190, 72.8420), 
    "T3-Andheri": (19.1137, 72.8632),
    "T4-Kurla": (19.0760, 72.8774)
}




# -----------------------------------
# Routes
# -----------------------------------



@app.route("/")
def home():
    return send_from_directory("static", "index.html")




@app.route("/api/forecast", methods=["POST"])
def forecast_load():
    try:
        data = request.json or {}
        horizon = int(data.get("horizon", 3))
        horizon = min(max(horizon, 1), 24)  # limit 1–24 hrs



        # Get weather forecast
        weather_data = get_mumbai_weather(horizon)



        # Get load predictions (sequential)
        predictions = predict_load(
            horizon,
            weather_data["temps"],
            weather_data["hums"]
        )



        peak_alert = max(predictions.values()) > 3500



        return jsonify({
            "success": True,
            "horizon": horizon,
            "timestamp": datetime.now().isoformat(),
            "weather": weather_data,
            "forecast": predictions,
            "peak_alert": peak_alert
        })



    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({"error": str(e)}), 500



@app.route("/api/transformers/<int:horizon>", methods=["GET"])
def get_transformer_status(horizon):
    """
    Transformer overload monitoring - YOUR model + location-specific weather!
    """
    try:
        # Mumbai-area transformers with coords & current loads
        transformers = [
            {"name": "T1-Bandra", "capacity": 2500, "current_load": 2100, "coords": TRANSFORMER_COORDS["T1-Bandra"]},
            {"name": "T2-Dadar", "capacity": 1800, "current_load": 1650, "coords": TRANSFORMER_COORDS["T2-Dadar"]},
            {"name": "T3-Andheri", "capacity": 2200, "current_load": 1950, "coords": TRANSFORMER_COORDS["T3-Andheri"]},
            {"name": "T4-Kurla", "capacity": 2000, "current_load": 1750, "coords": TRANSFORMER_COORDS["T4-Kurla"]}
        ]
        
        status = []
        
        for t in transformers:
            lat, lon = t["coords"]
            
            # LOCATION-SPECIFIC WEATHER for this substation!
            weather_data = get_weather_for_coords(lat, lon, horizon)
            
            # YOUR MODEL seeded with THIS transformer's current_load
            predictions = predict_load_custom_seed(
                horizon, weather_data["temps"], weather_data["hums"], t["current_load"]
            )
            
            peak_forecast = max(predictions.values())
            overload_pct = max(0, ((peak_forecast / t["capacity"]) * 100) - 100)
            
            # Risk & recommendations
            if overload_pct > 20:
                risk = "high"
                recs = ["IMMEDIATE: Shed 10-15% load", "Emergency cooling ON", "Reroute to spares", "Notify MERC"]
            elif overload_pct > 10:
                risk = "medium"
                recs = ["Balance feeder loads", "Aux cooling START", "Alert substation team"]
            else:
                risk = "low"
                recs = ["Continue monitoring", "Daily log"]
            
            status.append({
                "name": t["name"],
                "location": f"{lat:.4f}°N {lon:.4f}°E",
                "capacity": t["capacity"],
                "current_load": t["current_load"],
                "transformer_peak": round(peak_forecast, 1),
                "first_hour_temp": round(weather_data["temps"][0], 1),
                "overload_pct": round(overload_pct, 1),
                "risk": risk,
                "recommendations": recs
            })
        
        overall_risk = "high" if any(s["risk"] == "high" for s in status) else "medium" if any(s["risk"] == "medium" for s in status) else "low"
        
        return jsonify({
            "success": True,
            "horizon": horizon,
            "overall_risk": overall_risk,
            "transformers": status
        })
    
    except Exception as e:
        print(f"❌ Transformer API Error: {e}")
        return jsonify({"error": str(e)}), 500




# -----------------------------------
# Weather Functions
# -----------------------------------



def get_mumbai_weather(horizon):
    """
    Generic Mumbai central weather (for main forecast)
    """
    return get_weather_for_coords(19.0760, 72.8777, horizon)



def get_weather_for_coords(lat, lon, horizon):
    """
    HYPER-LOCAL OpenWeather for SPECIFIC substation coordinates!
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key: raise ValueError("API key missing")
        
        url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}&lon={lon}"
            f"&cnt={horizon}"
            f"&appid={api_key}"
            "&units=metric"
        )
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()["list"]
        temps = [item["main"]["temp"] for item in data]
        hums = [item["main"]["humidity"] for item in data]
        
        print(f"🌤️ {lat:.4f}°N {lon:.4f}°E: {horizon}h loaded")
        
        return {"temps": temps, "hums": hums}
    
    except Exception:
        print(f"🌤️ Demo data for {lat:.4f}°N {lon:.4f}°E ({horizon}h)")
        
        # Location-specific demo temps (urban heat variation)
        base_temp = 34.5 - (abs(lat - 19.0760) * 0.8)
        temps = np.linspace(base_temp, base_temp - 1.5, horizon).tolist()
        hums = np.linspace(75 + (abs(lon - 72.8777) * 2), 82, horizon).tolist()
        
        return {"temps": temps, "hums": hums}




# -----------------------------------
# Sequential Load Prediction
# -----------------------------------



def predict_load(horizon, temps, hums):
    """
    Generic system-wide forecast (unchanged!)
    """
    return predict_load_custom_seed(horizon, temps, hums, initial_load=2800)



def predict_load_custom_seed(horizon, temps, hums, initial_load=2800):
    """
    YOUR EXACT MODEL but with custom starting load (for transformers!)
    """
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    is_weekend = 1 if day_of_week >= 5 else 0
    
    predictions = {}
    previous_load = initial_load  # TRANSFORMER-SPECIFIC!
    
    for h in range(1, horizon + 1):
        i = min(h - 1, len(temps) - 1)
        temp = temps[i]
        hum = hums[i]
        
        # YOUR exact feature vector
        X = np.array([[hour, day_of_week, is_weekend, previous_load, temp, hum]])
        X_norm = model_data["scaler_X"].transform(X)
        y_norm = np.dot(X_norm, model_data["w"]) + model_data["b"]
        load = model_data["scaler_y"].inverse_transform(y_norm.reshape(1, -1))[0][0]
        
        predictions[f"load_lag_t+{h}"] = round(float(load), 1)
        previous_load = load  # Chain forward
        
        hour = (hour + 1) % 24
        if hour == 0:
            day_of_week = (day_of_week + 1) % 7
            is_weekend = 1 if day_of_week >= 5 else 0
    
    return predictions




# -----------------------------------
# Run Server
# -----------------------------------



if __name__ == "__main__":
    print("🚀 Mumbai Grid Forecaster + Hyper-Local Transformer Monitor running...")
    print("🌤️ Set OPENWEATHER_API_KEY for 4x substation-specific weather")
    print("⚡ YOUR ML model powers BOTH forecasts + transformer predictions")
    print("📊 Peak alert: 3500 MW | Transformers: /api/transformers/<h>")
    print("🌍 Server: http://localhost:5001")



    app.run(debug=True, port=5001, host="0.0.0.0")
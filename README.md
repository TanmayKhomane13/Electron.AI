<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=40&duration=3000&pause=800&color=00F0FF&center=true&vCenter=true&width=1000&lines=⚡+Electron.AI+⚡;Real-Time+Electricity+Demand+Forecasting;Smart+Grid+Decision+Intelligence" />

### Real-Time AI-Based Electricity Demand Forecasting for Smart Grids

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python">
  <img src="https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn">
  <img src="https://img.shields.io/badge/Pandas-Data-green?logo=pandas">
  <img src="https://img.shields.io/badge/NumPy-Computing-blue?logo=numpy">
  <img src="https://img.shields.io/badge/MAE-86.23MW-brightgreen">
</p>

> **Weather-aware, time-synchronized electricity demand forecasting system built for smart grid automation**

🚀 Generates multi-step forecasts in near real-time using historical demand data, live weather inputs, and system clock synchronization.

</div>

---

# 🔌 Project Overview

**Electron.AI** is a machine learning-based short-term load forecasting system designed for modern smart grid environments.

It integrates:

- 📊 Historical electricity demand data  
- 🌤️ Live weather data  
- ⏰ Real-time system clock  
- 📈 Multi-step forecasting (1, 2, 3 & upto 24 hours ahead)

The model is trained on historical patterns and deployed to generate forecasts aligned with real-world time.

---

# ⏰ Real-Time Automation Engine

Electron.AI operates using:

- The **current system time** of the deployed machine  
- Live weather conditions fetched at execution time  
- Trained historical demand patterns  
- Automated feature alignment with real-world timestamps  

Each prediction reflects **actual present time**, making the system:

✅ Production-realistic  
✅ Fully automated  
✅ Deployment-ready  
✅ Suitable for operational decision-making  

The entire system was **designed, developed, and coded completely from scratch**.

No automation platforms (like n8n).  
No workflow builders.  
No low-code orchestration tools.

---

# 🧠 Feature Engineering Logic (Current Version)

The current version is a **weather + calendar driven forecasting model trained on historical demand data**.

It learns relationships like:

```
(Historical Patterns + Time + Calendar + Weather) → Future Load
```

### Input Features

- Hour of day  
- Day of week  
- Weekend indicator  
- Holiday indicator  
- Temperature  
- Humidity
- Last Hour Demand (t - 1)

### Output Targets

- Load at t + 1 hour  
- Load at t + 2 hours  
- Load at t + 3 hours
- ...... 
- Load at t + 24 hours  

⚠️ Note:  
This version **includes autoregressive lag features (t-1 load input)** for sequential forecasting.  
Future iterations will expand to multiple lag features (t-2, t-3, etc.) for enhanced model accuracy.

---

# 🤖 Machine Learning Architecture

- Model Type: **Multi-Output Linear Regression**
- Forecast Horizon: 1, 2, 3 and upto 24 hours ahead in a single forward pass
- Built entirely from scratch

### 📊 Data Scaling

Scikit-Learn was used for:

- Scaling input features before training  
- Scaling output demand labels before regression  
- Inverse-transforming predictions back to MW scale  

This improves:

✅ Numerical stability  
✅ Convergence behavior  
✅ Model generalization  

The repository includes:

📁 `AIML/` folder  
- Jupyter Notebook  
- Training pipeline  
- Validation results  

All experimentation and evaluation were performed independently.

---

# 📊 Model Performance

| Metric | Value |
|--------|--------|
| **MAE** | **86.23 MW** |
| Forecast Horizon | 1, 2, 3 & upto 24 Hours |

---

## 📌 What 86.23 MW MAE Means

On average, predictions deviate by:

> **86.23 MW from actual electricity demand**

For grids operating between **2000–4000 MW**, this corresponds to:

⚡ Approximately **2–4% forecasting error**

This is considered efficient for short-term load forecasting systems using exogenous variables trained on historical data.

---

# 🎨 Frontend & UI

The frontend and UI were fully **Vibe Coded**.

Meaning:

- Clean and minimal admin workflow  
- Smooth interaction design  
- Fast visualization rendering  
- Built for quick decision-making  

Admin workflow:

```
Start Predicting → Enter Horizon and Last Hour Load → Instant Forecast Curve + Metrics
```

---

# 🧩 Tech Stack

### 🖥 Core Technologies

<p align="center"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="90" height="90" alt="Python"/> &nbsp;&nbsp;&nbsp; <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" width="90" height="90" alt="NumPy"/> &nbsp;&nbsp;&nbsp; <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" width="90" height="90" alt="Pandas"/> &nbsp;&nbsp;&nbsp; <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/matplotlib/matplotlib-original.svg" width="90" height="90" alt="Matplotlib"/> &nbsp;&nbsp;&nbsp; <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg" width="90" height="90" alt="Scikit-Learn"/> </p>

### 🌐 Additional Components

<p align="center">
  <img 
    src="https://cdn.simpleicons.org/flask/white"
    height="70"
    alt="Flask"
  />
  &nbsp;&nbsp;&nbsp;
  <img 
    src="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png"
    height="70"
    alt="OpenWeather API"
  />
</p>

---

# 🚨 Problem Context

🇮🇳 India consumes approximately **1.4 Trillion kWh annually**

Challenges:

- 15–20% daily demand uncertainty  
- Weather-driven load fluctuations  
- Manual forecasting delays  
- Grid imbalance losses ≈ ₹50,000 Cr/year  

---

# 💡 Our Solution

Electron.AI delivers:

🤖 Automated ML forecasting  
🌡️ Weather-aware demand modeling  
📚 Learning from historical demand patterns  
⏰ Real-time system synchronization  
📊 Instant visual analytics  
⚡ Near real-time predictions  

Designed to enable **quick and intelligent grid-level decision making.**

---

# 📸 Screenshots

<div align="center">

### 🔹 Home Page View
<img src="screenshots/1.png" width="800">
<img src="screenshots/2.png" width="800">

<br><br>

### 🔹 Forecast Page
<img src="screenshots/3.png" width="800">
<img src="screenshots/4.png" width="800">
<img src="screenshots/5.png" width="800">
<img src="screenshots/6.png" width="800">

<br><br>

### 🔹 Performance Metrics
<img src="screenshots/metrics.png" width="800">

</div>

---

# 🚀 Continuous Improvement

We are actively working on:

- Improving MAE beyond 86.23MW
- Implementing smart peak-load alerts  
- Enabling real-time smart meter streaming  

The goal is to evolve Electron.AI into a complete:

> ⚡ Decision Intelligence Engine for Smart Grids

---

<div align="center">

### ⚡ Powering Smart Grids with Intelligent Forecasting  

---

## 📜 Copyright

© 2026 Tanmay Khomane and Atharva Jejurkar

Developed with ⚡ for intelligent smart grid forecasting.  
All rights reserved.

</div>

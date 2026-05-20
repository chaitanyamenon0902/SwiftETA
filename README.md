<div align="center">

<img src="frontend/src/assets/logoswifteta.png" width="180"/>

# SwiftETA

### AI-Powered Smart Delivery ETA Prediction Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/XGBoost-ML-FF6600?style=for-the-badge&logo=xgboost&logoColor=white"/>
  <img src="https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white"/>
  <img src="https://img.shields.io/badge/Render-Backend-46E3B7?style=for-the-badge&logo=render&logoColor=black"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-CC2927?style=flat-square&logo=databricks&logoColor=white"/>
  <img src="https://img.shields.io/badge/WebSockets-Live-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenStreetMap-API-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white"/>
</p>

<br/>

> **SwiftETA** is a production-grade AI-powered delivery ETA prediction platform inspired by real-world logistics systems such as Swiggy and Zomato. It combines Machine Learning, geospatial intelligence, live traffic signals, and weather-aware prediction pipelines to generate highly accurate delivery ETAs through a modern full-stack architecture.

<br/>

**[Live Demo](https://swifteta.vercel.app)** • **[API Docs](https://swift-eta.onrender.com/docs)** • **[Report Bug](../../issues)** • **[Request Feature](../../issues)**

</div>

---

# Overview

SwiftETA is an end-to-end Machine Learning system designed to solve one of the most important problems in logistics engineering: accurate last-mile delivery ETA prediction.

The platform integrates:

- Machine Learning-based ETA inference
- Traffic-aware predictions
- Weather-aware routing intelligence
- Interactive geospatial visualization
- Real-time WebSocket updates
- Analytics dashboards
- Feedback-driven model improvement

The project was built to reflect production-oriented software engineering and ML system design principles rather than a basic demo application.

---

# Features

| Category | Capability |
|---|---|
| Machine Learning | Real-time ETA prediction using XGBoost |
| Geospatial Intelligence | Haversine distance computation |
| Traffic Awareness | Congestion-aware ETA adjustments |
| Weather Awareness | Weather-conditioned predictions |
| Real-Time Updates | FastAPI WebSocket streaming |
| Mapping | Interactive delivery visualization using React-Leaflet |
| Analytics | Dashboard powered by Recharts |
| Backend APIs | FastAPI REST architecture |
| Monitoring | Model metrics & analytics endpoints |
| Deployment | Frontend on Vercel, Backend on Render |

---

# Screenshots

<div align="center">

| Live Tracking Map | Analytics Dashboard |
|---|---|
| ![](docs/screenshots/map-view.png) | ![](docs/screenshots/dashboard.png) |

| ETA Prediction Panel | Model Metrics Monitor |
|---|---|
| ![](docs/screenshots/prediction.png) | ![](docs/screenshots/metrics.png) |

</div>

> Add your screenshots inside `docs/screenshots/`

---

# System Architecture

```text
Frontend (React + Vite + Tailwind)
        │
        ▼
 REST API + WebSocket Communication
        │
        ▼
Backend (FastAPI + SQLAlchemy)
        │
        ▼
Machine Learning Inference Engine
(XGBoost / Scikit-learn)
        │
        ▼
SQLite Database + Model Artifacts
```

---

# Machine Learning Pipeline

```text
Input Features
│
├── Pickup Coordinates
├── Drop Coordinates
├── Traffic Density
├── Weather Conditions
├── Rider Rating
├── Order Type
└── Time of Day
        │
        ▼
Feature Engineering
        │
        ▼
XGBoost Regressor
        │
        ▼
Predicted ETA Output
        │
        ▼
Feedback Loop for Retraining
```

## Model Comparison

| Model | MAE | Status |
|---|---|---|
| Linear Regression | ~8.2 mins | Baseline |
| Random Forest | ~4.1 mins | Candidate |
| XGBoost | ~2.8 mins | Selected |

XGBoost was selected because of its strong performance on structured delivery datasets and fast inference suitable for real-time prediction APIs.

---

# Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React.js, Vite, Tailwind CSS, Axios, React-Leaflet, Recharts |
| Backend | FastAPI, SQLAlchemy, WebSockets, Pydantic |
| Machine Learning | Scikit-learn, XGBoost, Pandas, NumPy, Joblib |
| Database | SQLite |
| Deployment | Vercel, Render |

---

# Project Structure

```text
SwiftETA/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── components/
│
├── backend/
│   ├── database/
│   ├── models/
│   ├── ml/
│   └── app.py
│
├── docs/
│   └── screenshots/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# API Reference

## Base URL

```text
https://swift-eta.onrender.com
```

## Core Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict_eta` | Generate ETA prediction |
| GET | `/analytics` | Delivery analytics |
| GET | `/model/metrics` | ML model performance metrics |
| POST | `/submit_feedback` | Submit actual delivery feedback |
| WS | `/ws/live-updates` | Real-time WebSocket updates |

---

# Deployment

| Service | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| API Documentation | Swagger / OpenAPI |

## Live Links

### Frontend

```text
https://swifteta.vercel.app
```

### Backend API

```text
https://swift-eta.onrender.com
```

### Swagger Documentation

```text
https://swift-eta.onrender.com/docs
```

---

# System Workflow

```text
User Inputs Delivery Details
            │
            ▼
Frontend Sends API Request
            │
            ▼
FastAPI Backend Validates Request
            │
            ▼
Feature Engineering Pipeline
            │
            ▼
ML Model Generates ETA
            │
            ▼
Prediction Stored in Database
            │
            ▼
Frontend Receives ETA + Live Updates
```

---

# Challenges & Solutions

| Challenge | Solution |
|---|---|
| Cross-origin deployment issues | Configured FastAPI CORS middleware |
| Render cold-start latency | Optimized lightweight model inference |
| Real-time synchronization | Implemented WebSocket broadcasting |
| Geospatial approximation | Added Haversine distance calculation |
| Model drift | Built feedback collection pipeline |

---

# Future Improvements

- PostgreSQL migration
- Dockerized deployment
- JWT authentication
- Google Maps integration
- MLflow experiment tracking
- Rider mobile application
- Real-time traffic APIs
- Automated retraining pipelines

---

# Learning Outcomes

SwiftETA provided practical experience in:

- Full-stack architecture design
- Machine Learning deployment
- FastAPI backend engineering
- WebSocket communication
- Cloud deployment workflows
- Geospatial computation
- REST API development
- Model inference optimization


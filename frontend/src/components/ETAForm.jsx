import { useState } from "react";
import { predictETA } from "../services/api";
import FeedbackForm from "./FeedbackForm";

// 🔔 ADDED: 'onPredictionSuccess' prop to talk to your Dashboard component
function ETAForm({ onPredictionSuccess }) {
  const [form, setForm] = useState({
    restaurant_latitude: "",
    restaurant_longitude: "",
    customer_latitude: "",
    customer_longitude: "",
    rider_name: "",
    rider_age: "",
    rider_rating: "",
    order_type: "Meal",
    vehicle_type: "Bike",
    order_timestamp: new Date().toISOString(),
    traffic_level: 5,
    weather_condition: "Clear",
  });

  const [eta, setEta] = useState(null);
  const [predictionId, setPredictionId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        ...form,
        restaurant_latitude: parseFloat(form.restaurant_latitude),
        restaurant_longitude: parseFloat(form.restaurant_longitude),
        customer_latitude: parseFloat(form.customer_latitude),
        customer_longitude: parseFloat(form.customer_longitude),
        rider_age: parseInt(form.rider_age) || 0, // Fallback if left blank
        rider_rating: parseFloat(form.rider_rating) || 0.0,
        traffic_level: parseInt(form.traffic_level),
      };

      console.log("📤 [ETAForm] Firing API request with payload:", payload);
      const res = await predictETA(payload);
      
      // 1. Keep local states happy for internal panels and feedback
      setEta(res.predicted_eta_minutes);
      setPredictionId(res.prediction_id);

      // 2. 🔔 CRITICAL: Forward the backend response up to Dashboard.jsx
      if (onPredictionSuccess) {
        console.log("🚀 [ETAForm] Bubbling backend response to parent Dashboard...");
        onPredictionSuccess(res);
      }

    } catch (err) {
      console.error("❌ [ETAForm] Prediction failed:", err);
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  // UI Constants matching PredictionPanel
  const inputClass = "w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white transition focus:border-blue-500 outline-none";
  const labelClass = "block text-sm text-slate-400 mb-2";

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white">Swift ETA Predictor</h2>
        <p className="text-slate-400 text-sm mt-1">
          AI-powered real-time delivery intelligence
        </p>
      </div>

      <form onSubmit={submit} className="space-y-5">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Restaurant Latitude</label>
            <input name="restaurant_latitude" placeholder="12.9716" onChange={handleChange} className={inputClass} required />
          </div>
          <div>
            <label className={labelClass}>Restaurant Longitude</label>
            <input name="restaurant_longitude" placeholder="77.5946" onChange={handleChange} className={inputClass} required />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Delivery Latitude</label>
            <input name="customer_latitude" placeholder="12.9352" onChange={handleChange} className={inputClass} required />
          </div>
          <div>
            <label className={labelClass}>Delivery Longitude</label>
            <input name="customer_longitude" placeholder="77.6245" onChange={handleChange} className={inputClass} required />
          </div>
        </div>

        <div>
          <label className={labelClass}>Rider & Rating</label>
          <div className="grid grid-cols-3 gap-3">
            <input name="rider_name" placeholder="Name" onChange={handleChange} className={inputClass} />
            <input name="rider_age" placeholder="Age" type="number" onChange={handleChange} className={inputClass} />
            <input name="rider_rating" placeholder="Rating" type="number" step="0.1" onChange={handleChange} className={inputClass} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Order Type</label>
            <select name="order_type" value={form.order_type} onChange={handleChange} className={inputClass}>
              <option value="Meal">Meal</option>
              <option value="Drink">Drink</option>
              <option value="Snack">Snack</option>
            </select>
          </div>
          <div>
            <label className={labelClass}>Vehicle Type</label>
            <select name="vehicle_type" value={form.vehicle_type} onChange={handleChange} className={inputClass}>
              <option value="Bike">Bike</option>
              <option value="Scooter">Scooter</option>
              <option value="Bicycle">Bicycle</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-3 font-semibold transition disabled:opacity-50"
        >
          {loading ? 'Predicting...' : 'Predict ETA'}
        </button>
      </form>

      {eta && (
        <div className="mt-6 bg-slate-950 border border-slate-800 rounded-xl p-5">
          <p className="text-slate-400 text-sm">Predicted Delivery ETA</p>
          <h1 className="text-5xl font-bold text-white mt-2">
            {eta} mins
          </h1>

          <div className="grid grid-cols-2 gap-4 mt-5">
            <div className="bg-slate-900 rounded-lg p-4">
              <p className="text-slate-400 text-xs">Route Condition</p>
              <h3 className="text-xl font-bold text-yellow-400 mt-1">Live Tracking</h3>
            </div>
            <div className="bg-slate-900 rounded-lg p-4">
              <p className="text-slate-400 text-xs">Delivery Status</p>
              <h3 className="text-xl font-bold text-green-400 mt-1">On Track</h3>
            </div>
          </div>

          {predictionId && (
            <div className="mt-6 pt-6 border-t border-slate-800">
              <FeedbackForm predictionId={predictionId} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ETAForm;
import { useEffect, useState } from "react";
import Navbar from "./Navbar";
import KPICards from "./KPICards";
import ETAForm from "./ETAForm";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import L from "leaflet";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

import { getAnalytics, getModelMetrics } from "../services/api";

// =====================
// LEAFLET ICON FIX
// =====================
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

// =====================
// MAP UPDATER
// =====================
function MapUpdater({ restaurant, customer }) {
  const map = useMap();

  useEffect(() => {
    if (!restaurant || !customer) return;
    map.fitBounds([restaurant, customer], { padding: [80, 80] });
  }, [restaurant, customer]);

  return null;
}

// =====================
// MAIN DASHBOARD
// =====================
function Dashboard() {
  const [analytics, setAnalytics] = useState({});
  const [metrics, setMetrics] = useState({});
  const [loading, setLoading] = useState(false); // Keeps track of layout UI sync if needed

  const [mapCoords, setMapCoords] = useState({
    restaurant: null,
    customer: null
  });

  const [city, setCity] = useState("Unknown City");
  const [weather, setWeather] = useState(null);
  const [trafficData, setTrafficData] = useState([]);

  // =====================
  // INIT DATA
  // =====================
  useEffect(() => {
    (async () => {
      try {
        setAnalytics(await getAnalytics());
        setMetrics(await getModelMetrics());
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  // =====================
  // TRAFFIC INDEX
  // =====================
  const trafficMultiplier = (level) => {
    switch (Number(level)) {
      case 1: return 1.1;
      case 2: return 1.4;
      case 3: return 1.8;
      default: return 1.2;
    }
  };

  // =====================
  // CITY INTELLIGENCE (weather + traffic)
  // =====================
  const fetchCityIntelligence = async (lat, lng, trafficLevel, cityName) => {
    try {
      setCity(cityName || "Detected Route");

      const base = trafficMultiplier(trafficLevel);

      setTrafficData([
        { zone: "Central", index: base * 1.3 },
        { zone: "North", index: base * 1.1 },
        { zone: "South", index: base * 0.9 },
        { zone: "East", index: base * 1.05 },
        { zone: "West", index: base * 1.2 }
      ]);

      const res = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&current_weather=true`
      );

      const data = await res.json();
      setWeather(data.current_weather);
    } catch (err) {
      console.error("City intelligence error:", err);
    }
  };

  // =====================
  // 🔔 FIXED PREDICT FLOW RECEIVER
  // =====================
  const handlePredictionSuccess = async (res) => {
    if (!res || res.status === "error") {
      console.error("Malformed payload received in Dashboard");
      return;
    }

    console.log("📥 [Dashboard] Intercepted successful prediction backend data:", res);

    try {
      // 1. UPDATE LEAFLET MAP COORDINATES
      setMapCoords({
        restaurant: [
          res.restaurant_latitude,
          res.restaurant_longitude
        ],
        customer: [
          res.customer_latitude,
          res.customer_longitude
        ]
      });

      // 2. TRIGGER EXTRACTION FOR WEATHER & TRAFFIC
      // Default to 5 if traffic_level isn't mirrored cleanly back by your custom backend
      const responseTrafficLevel = res.traffic_level ?? 5; 

      await fetchCityIntelligence(
        res.customer_latitude,
        res.customer_longitude,
        responseTrafficLevel,
        res.city
      );

    } catch (err) {
      console.error("Error setting visual metrics layouts in dashboard:", err);
    }
  };

  // =====================
  // MAP COMPONENT (INLINE)
  // =====================
  const DeliveryMap = () => {
    if (!mapCoords.restaurant || !mapCoords.customer) {
      return (
        <div className="h-[500px] flex items-center justify-center text-gray-400 border border-slate-800 bg-slate-900 rounded-xl">
          Waiting for route...
        </div>
      );
    }

    return (
      <div className="h-[500px] rounded-xl overflow-hidden border border-slate-800">
        <MapContainer
          center={mapCoords.restaurant}
          zoom={12}
          className="h-full w-full"
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapUpdater
            restaurant={mapCoords.restaurant}
            customer={mapCoords.customer}
          />

          <Marker position={mapCoords.restaurant}>
            <Popup>Restaurant</Popup>
          </Marker>

          <Marker position={mapCoords.customer}>
            <Popup>Customer</Popup>
          </Marker>

          <Polyline
            positions={[
              mapCoords.restaurant,
              mapCoords.customer
            ]}
            color="#3b82f6"
            weight={4}
          />
        </MapContainer>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />

      <div className="p-6 space-y-6">
        <KPICards analytics={analytics} metrics={metrics} />

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div>
            {/* 🔔 MOUNTED UPDATED PROP PROPAGATION HERE */}
            <ETAForm onPredictionSuccess={handlePredictionSuccess} />
          </div>

          <div className="xl:col-span-2">
            <DeliveryMap />
          </div>
        </div>

        {/* TRAFFIC */}
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <h2 className="text-xl font-bold mb-4">{city} Traffic Index</h2>

          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={trafficData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="zone" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }}
                labelStyle={{ color: '#fff' }}
              />
              <Bar dataKey="index" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* WEATHER */}
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl grid grid-cols-2 gap-4">
          <div>
            <h2 className="text-xl font-bold mb-2">Environmental Data</h2>
            <p className="text-slate-400">Current Area: <span className="text-white font-medium">{city}</span></p>
          </div>
          <div className="flex justify-around items-center bg-slate-950 border border-slate-800 rounded-lg p-4">
            <p className="text-sm text-slate-400">Temp: <span className="text-xl font-bold text-blue-400">{weather?.temperature ?? "--"} °C</span></p>
            <p className="text-sm text-slate-400">Wind: <span className="text-xl font-bold text-blue-400">{weather?.windspeed ?? "--"} km/h</span></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
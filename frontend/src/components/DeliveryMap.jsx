import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useMemo } from "react";
import L from "leaflet";

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

// ===============================
// MAP AUTO ZOOM CONTROLLER
// ===============================
function MapUpdater({ restaurant, customer }) {
  const map = useMap();

  useEffect(() => {
    if (!restaurant || !customer) return;

    map.flyToBounds([restaurant, customer], {
      padding: [80, 80],
      duration: 1.5
    });
  }, [restaurant, customer, map]);

  return null;
}

// ===============================
// MAIN COMPONENT
// ===============================
function DeliveryMap({
  restaurantLat,
  restaurantLng,
  customerLat,
  customerLng
}) {

  const restaurant =
    restaurantLat != null && restaurantLng != null
      ? [Number(restaurantLat), Number(restaurantLng)]
      : null;

  const customer =
    customerLat != null && customerLng != null
      ? [Number(customerLat), Number(customerLng)]
      : null;

  return (
    <div className="h-[500px] rounded-xl overflow-hidden border border-slate-800 relative z-0">
      <MapContainer
        center={restaurant || [20.5937, 78.9629]} // fallback India center
        zoom={5}
        scrollWheelZoom={true}
        className="h-full w-full"
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* only fly when both exist */}
        {restaurant && customer && (
          <MapUpdater restaurant={restaurant} customer={customer} />
        )}

        {/* markers only render when data exists */}
        {restaurant && (
          <Marker position={restaurant}>
            <Popup>🍴 Restaurant</Popup>
          </Marker>
        )}

        {customer && (
          <Marker position={customer}>
            <Popup>🏠 Delivery</Popup>
          </Marker>
        )}

        {/* route line only when both exist */}
        {restaurant && customer && (
          <Polyline
            positions={[restaurant, customer]}
            pathOptions={{
              color: "#3b82f6",
              weight: 5,
              opacity: 0.8
            }}
          />
        )}

      </MapContainer>
    </div>
  );
}
export default DeliveryMap;
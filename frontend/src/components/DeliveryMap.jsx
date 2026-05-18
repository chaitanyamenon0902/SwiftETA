import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline
} from 'react-leaflet'

import 'leaflet/dist/leaflet.css'

export default function DeliveryMap() {

  const restaurant = [12.9716, 77.5946]
  const customer = [12.9352, 77.6245]

  return (
    <div className="h-[500px] rounded-xl overflow-hidden border border-slate-800">

      <MapContainer
        center={[12.9716, 77.5946]}
        zoom={12}
        className="h-full w-full"
      >

        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <Marker position={restaurant}>
          <Popup>
            Restaurant
          </Popup>
        </Marker>

        <Marker position={customer}>
          <Popup>
            Customer
          </Popup>
        </Marker>

        <Polyline positions={[restaurant, customer]} />

      </MapContainer>
    </div>
  )
}
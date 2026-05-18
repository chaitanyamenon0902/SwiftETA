import { useState } from 'react'
import { predictETA } from '../services/api'

export default function PredictionPanel() {

  const [formData, setFormData] = useState({

    restaurant_latitude: '',
    restaurant_longitude: '',

    customer_latitude: '',
    customer_longitude: '',

    rider_id: '',

    traffic_level: 5
  })

  const [prediction, setPrediction] = useState(null)

  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {

    e.preventDefault()

    setLoading(true)

    try {

      const payload = {

        restaurant_latitude: parseFloat(
          formData.restaurant_latitude
        ),

        restaurant_longitude: parseFloat(
          formData.restaurant_longitude
        ),

        customer_latitude: parseFloat(
          formData.customer_latitude
        ),

        customer_longitude: parseFloat(
          formData.customer_longitude
        ),

        rider_id: parseInt(
          formData.rider_id
        ),

        traffic_level: parseInt(
          formData.traffic_level
        )
      }

      const result = await predictETA(payload)

      setPrediction(result)

    } catch (error) {

      console.error('Prediction Error:', error)

    } finally {

      setLoading(false)
    }
  }

  return (

    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">

      <div className="mb-6">

        <h2 className="text-2xl font-bold text-white">
          ETA Prediction Engine
        </h2>

        <p className="text-slate-400 text-sm mt-1">
          Real-time delivery intelligence
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-5"
      >

        <div>

          <label className="block text-sm text-slate-400 mb-2">
            Restaurant Latitude
          </label>

          <input
            type="number"
            step="any"
            name="restaurant_latitude"
            placeholder="12.9716"
            value={formData.restaurant_latitude}
            onChange={handleChange}
            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-lg
              px-4
              py-3
              text-white
              outline-none
              focus:border-blue-500
            "
            required
          />
        </div>

        <div>

          <label className="block text-sm text-slate-400 mb-2">
            Restaurant Longitude
          </label>

          <input
            type="number"
            step="any"
            name="restaurant_longitude"
            placeholder="77.5946"
            value={formData.restaurant_longitude}
            onChange={handleChange}
            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-lg
              px-4
              py-3
              text-white
              outline-none
              focus:border-blue-500
            "
            required
          />
        </div>

        <div>

          <label className="block text-sm text-slate-400 mb-2">
            Drop Latitude
          </label>

          <input
            type="number"
            step="any"
            name="customer_latitude"
            placeholder="12.9352"
            value={formData.customer_latitude}
            onChange={handleChange}
            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-lg
              px-4
              py-3
              text-white
              outline-none
              focus:border-blue-500
            "
            required
          />
        </div>

        <div>

          <label className="block text-sm text-slate-400 mb-2">
            Drop Longitude
          </label>

          <input
            type="number"
            step="any"
            name="customer_longitude"
            placeholder="77.6245"
            value={formData.customer_longitude}
            onChange={handleChange}
            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-lg
              px-4
              py-3
              text-white
              outline-none
              focus:border-blue-500
            "
            required
          />
        </div>

        <div>

          <label className="block text-sm text-slate-400 mb-2">
            Rider ID
          </label>

          <input
            type="number"
            name="rider_id"
            placeholder="421"
            value={formData.rider_id}
            onChange={handleChange}
            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-lg
              px-4
              py-3
              text-white
              outline-none
              focus:border-blue-500
            "
            required
          />
        </div>

        <div>

          <div className="flex items-center justify-between mb-2">

            <label className="text-sm text-slate-400">
              Traffic Level
            </label>

            <span className="text-blue-400 text-sm font-semibold">
              {formData.traffic_level}
            </span>
          </div>

          <input
            type="range"
            min="1"
            max="10"
            name="traffic_level"
            value={formData.traffic_level}
            onChange={handleChange}
            className="w-full"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="
            w-full
            bg-blue-600
            hover:bg-blue-700
            transition
            rounded-lg
            py-3
            text-white
            font-semibold
          "
        >

          {loading
            ? 'Predicting...'
            : 'Predict ETA'}
        </button>
      </form>

      {prediction && (

        <div className="
          mt-6
          bg-slate-950
          border
          border-slate-800
          rounded-xl
          p-5
        ">

          <p className="text-slate-400 text-sm">
            Predicted Delivery ETA
          </p>

          <h1 className="text-5xl font-bold text-white mt-2">
            {prediction.predicted_eta_minutes} mins
          </h1>

          <div className="grid grid-cols-2 gap-4 mt-5">

            <div className="
              bg-slate-900
              rounded-lg
              p-4
            ">

              <p className="text-slate-400 text-xs">
                Traffic Impact
              </p>

              <h3 className="text-xl font-bold text-white mt-1">
                High
              </h3>
            </div>

            <div className="
              bg-slate-900
              rounded-lg
              p-4
            ">

              <p className="text-slate-400 text-xs">
                Delivery Status
              </p>

              <h3 className="text-xl font-bold text-green-400 mt-1">
                On Track
              </h3>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
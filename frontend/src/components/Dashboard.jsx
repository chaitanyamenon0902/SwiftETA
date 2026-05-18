import { useEffect, useState } from 'react'

import Navbar from './Navbar'
import KPICards from './KPICards'
import PredictionPanel from './PredictionPanel'
import DeliveryMap from './DeliveryMap'
import LiveEventFeed from './LiveEventFeed'

import useWebSocket from '../hooks/useWebSocket'

import {
  getAnalytics,
  getModelMetrics
} from '../services/api'

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  AreaChart,
  Area,
  BarChart,
  Bar
} from 'recharts'

function Dashboard() {

  const [analytics, setAnalytics] = useState({})
  const [metrics, setMetrics] = useState({})

  const [events, setEvents] = useState([])

  const [etaHistory, setEtaHistory] = useState([
    { time: '10:00', eta: 24 },
    { time: '10:05', eta: 26 },
    { time: '10:10', eta: 28 },
    { time: '10:15', eta: 25 },
    { time: '10:20', eta: 31 },
    { time: '10:25', eta: 29 }
  ])

  const [trafficData] = useState([
    { zone: 'North', traffic: 4 },
    { zone: 'South', traffic: 7 },
    { zone: 'East', traffic: 6 },
    { zone: 'West', traffic: 8 },
    { zone: 'Central', traffic: 9 }
  ])

  useEffect(() => {

    fetchDashboardData()

    const interval = setInterval(() => {
      fetchDashboardData()
    }, 10000)

    return () => clearInterval(interval)

  }, [])

  const fetchDashboardData = async () => {

    try {

      const analyticsData = await getAnalytics()
      const metricsData = await getModelMetrics()

      setAnalytics(analyticsData)
      setMetrics(metricsData)

    } catch (error) {

      console.error('Dashboard fetch error:', error)
    }
  }

  useWebSocket((event) => {

    setEvents((prev) => [event, ...prev.slice(0, 14)])

    setEtaHistory((prev) => {

      const next = [
        ...prev,
        {
          time: new Date().toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
          }),
          eta: Math.floor(Math.random() * 15) + 20
        }
      ]

      return next.slice(-8)
    })
  })

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      <Navbar />

      <div className="p-6 space-y-6">

        <KPICards
          analytics={analytics}
          metrics={metrics}
        />

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

          <div className="xl:col-span-1">
            <PredictionPanel />
          </div>

          <div className="xl:col-span-2">
            <DeliveryMap />
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

            <div className="flex items-center justify-between mb-4">

              <div>
                <h2 className="text-xl font-bold">
                  Live ETA Trend
                </h2>

                <p className="text-slate-400 text-sm">
                  Real-time prediction movement
                </p>
              </div>
            </div>

            <div className="h-[320px]">

              <ResponsiveContainer width="100%" height="100%">

                <LineChart data={etaHistory}>

                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

                  <XAxis
                    dataKey="time"
                    stroke="#94a3b8"
                  />

                  <YAxis
                    stroke="#94a3b8"
                  />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="eta"
                    strokeWidth={3}
                  />

                </LineChart>

              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

            <div className="flex items-center justify-between mb-4">

              <div>
                <h2 className="text-xl font-bold">
                  Traffic Heatmap
                </h2>

                <p className="text-slate-400 text-sm">
                  City-wide congestion intelligence
                </p>
              </div>
            </div>

            <div className="h-[320px]">

              <ResponsiveContainer width="100%" height="100%">

                <BarChart data={trafficData}>

                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

                  <XAxis
                    dataKey="zone"
                    stroke="#94a3b8"
                  />

                  <YAxis
                    stroke="#94a3b8"
                  />

                  <Tooltip />

                  <Bar
                    dataKey="traffic"
                  />

                </BarChart>

              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

          <div className="xl:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">

            <div className="mb-5">

              <h2 className="text-xl font-bold">
                Delivery Performance
              </h2>

              <p className="text-slate-400 text-sm">
                Operational delivery analytics
              </p>
            </div>

            <div className="h-[320px]">

              <ResponsiveContainer width="100%" height="100%">

                <AreaChart data={etaHistory}>

                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

                  <XAxis
                    dataKey="time"
                    stroke="#94a3b8"
                  />

                  <YAxis
                    stroke="#94a3b8"
                  />

                  <Tooltip />

                  <Area
                    type="monotone"
                    dataKey="eta"
                    strokeWidth={2}
                  />

                </AreaChart>

              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

            <div className="mb-5">

              <h2 className="text-xl font-bold">
                Live Event Feed
              </h2>

              <p className="text-slate-400 text-sm">
                Real-time operational updates
              </p>
            </div>

            <LiveEventFeed events={events} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
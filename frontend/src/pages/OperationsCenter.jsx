import { useEffect, useState } from 'react'

import Navbar from '../components/Navbar'
import KPICards from '../components/KPICards'
import AnalyticsChart from '../components/AnalyticsChart'
import DeliveryMap from '../components/DeliveryMap'
import PredictionPanel from '../components/PredictionPanel'
import LiveEventFeed from '../components/LiveEventFeed'
import TrafficHeatmap from '../components/TrafficHeatmap'
import MonitoringPanel from '../components/MonitoringPanel'
import WebSocketStatus from '../components/WebSocketStatus'
import LoadingScreen from '../components/LoadingScreen'

import { useWebSocket } from '../hooks/useWebSocket'

import {
  getAnalytics,
  getModelMetrics,
  getHealth,
} from '../services/api'

function OperationsCenter() {
  const {
    connected,
    riderPositions,
    trafficZones,
    liveEvents,
    kpiData,
    sendMessage,
  } = useWebSocket()

  const [analytics, setAnalytics] = useState(null)
  const [modelMetrics, setModelMetrics] = useState(null)
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const [analyticsRes, metricsRes, healthRes] =
          await Promise.all([
            getAnalytics(),
            getModelMetrics(),
            getHealth(),
          ])

        setAnalytics(analyticsRes.data)
        setModelMetrics(metricsRes.data)
        setHealth(healthRes.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadData()

    const interval = setInterval(loadData, 30000)

    return () => clearInterval(interval)
  }, [])

  if (loading) return <LoadingScreen />

  return (
    <div className="min-h-screen bg-[#060B18] text-slate-200 p-6">
      <div className="max-w-[1700px] mx-auto space-y-6">
        <Navbar connected={connected} health={health} />

        <KPICards
          kpiData={kpiData}
          modelMetrics={modelMetrics}
        />

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          <div className="xl:col-span-8 space-y-6">
            <div className="glass-card p-5">
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-xl font-semibold text-cyan-400">
                  Live Delivery Network
                </h2>

                <WebSocketStatus connected={connected} />
              </div>

              <DeliveryMap
                riderPositions={riderPositions}
                trafficZones={trafficZones}
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="glass-card p-5">
                <h2 className="text-lg font-semibold mb-4 text-cyan-400">
                  Delivery Analytics
                </h2>

                <AnalyticsChart data={analytics} />
              </div>

              <div className="glass-card p-5">
                <h2 className="text-lg font-semibold mb-4 text-cyan-400">
                  Traffic Heatmap
                </h2>

                <TrafficHeatmap zones={trafficZones} />
              </div>
            </div>
          </div>

          <div className="xl:col-span-4 space-y-6">
            <div className="glass-card p-5">
              <h2 className="text-lg font-semibold mb-4 text-cyan-400">
                ETA Prediction Engine
              </h2>

              <PredictionPanel />
            </div>

            <div className="glass-card p-5 h-[500px] overflow-hidden">
              <h2 className="text-lg font-semibold mb-4 text-cyan-400">
                Live Event Feed
              </h2>

              <LiveEventFeed events={liveEvents} />
            </div>

            <div className="glass-card p-5">
              <h2 className="text-lg font-semibold mb-4 text-cyan-400">
                System Monitoring
              </h2>

              <MonitoringPanel
                connected={connected}
                health={health}
                metrics={modelMetrics}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default OperationsCenter;
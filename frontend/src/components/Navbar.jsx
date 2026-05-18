function Navbar() {

  return (
    <div className="h-16 border-b border-slate-800 bg-slate-950 flex items-center justify-between px-6">

      <div>
        <h1 className="text-2xl font-bold text-white">
          SWIFT-ETA
        </h1>

        <p className="text-slate-400 text-sm">
          Real-Time Logistics Intelligence Platform
        </p>
      </div>

      <div className="flex items-center gap-2">
        <div className="h-3 w-3 bg-green-500 rounded-full animate-pulse"></div>

        <span className="text-green-400 text-sm">
          LIVE
        </span>
      </div>
    </div>
  )
}

export default Navbar
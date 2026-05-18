function WebSocketStatus({ connected }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      <span
        className={`status-dot ${
          connected ? 'bg-green-400' : 'bg-red-400'
        }`}
      />

      <span className="text-slate-400">
        {connected ? 'Live Stream Active' : 'Disconnected'}
      </span>
    </div>
  )
}

export default WebSocketStatus
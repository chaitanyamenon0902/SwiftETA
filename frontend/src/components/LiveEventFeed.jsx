function LiveEventFeed({ events }) {

  return (
    <div className="space-y-3 h-[500px] overflow-y-auto">

      {events.map((event, index) => (

        <div
          key={index}
          className="bg-slate-900 border border-slate-800 rounded-xl p-4"
        >

          <div className="flex items-center justify-between">

            <h3 className="text-white font-semibold">
              {event.eventType}
            </h3>

            <span className="text-slate-500 text-xs">
              {event.time}
            </span>
          </div>

          <p className="text-slate-400 text-sm mt-2">
            {event.message}
          </p>
        </div>
      ))}
    </div>
  )
}

export default LiveEventFeed
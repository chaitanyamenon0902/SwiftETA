function KPICards({ analytics, metrics }) {

  const cards = [
    {
      title: 'Active Orders',
      value: analytics?.active_orders || 0
    },
    {
      title: 'Average ETA',
      value: `${analytics?.avg_eta || 0} mins`
    },
    {
      title: 'Traffic Index',
      value: analytics?.traffic_index || 0
    },
    {
      title: 'Prediction Accuracy',
      value: `${analytics?.prediction_accuracy || 0}%`
    },
    {
      title: 'RMSE',
      value: metrics?.rmse || 0
    },
    {
      title: 'MAE',
      value: metrics?.mae || 0
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-6 gap-4">

      {cards.map((card, index) => (

        <div
          key={index}
          className="bg-slate-900 border border-slate-800 rounded-xl p-5"
        >
          <p className="text-slate-400 text-sm">
            {card.title}
          </p>

          <h2 className="text-2xl font-bold text-white mt-2">
            {card.value}
          </h2>
        </div>
      ))}
    </div>
  )
}


export default KPICards
export const createWebSocket = (onMessage) => {

  const socket = new WebSocket(
    'ws://127.0.0.1:8000/ws/live-updates'
  )

  socket.onopen = () => {
    console.log('WebSocket Connected')
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }

  socket.onerror = (error) => {
    console.error('WebSocket Error:', error)
  }

  socket.onclose = () => {
    console.log('WebSocket Closed')
  }

  return socket
}
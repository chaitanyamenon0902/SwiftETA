export const createWebSocket = (onMessage) => {
  // 1. Determine if we are running in production on Vercel
  const isProduction = import.meta.env?.PROD || process.env?.NODE_ENV === 'production';

  const WS_URL = isProduction
    ? 'wss://swift-eta.onrender.com/ws/live-updates'
    : 'ws://127.0.0.1:8000/ws/live-updates';

  const socket = new WebSocket(WS_URL);

  socket.onopen = () => {
    console.log('WebSocket Connected');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (err) {
      console.error('Error parsing WebSocket message data:', err);
    }
  };

  socket.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };

  socket.onclose = () => {
    console.log('WebSocket Closed');
  };

  return socket;
};
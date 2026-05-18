import { useEffect } from 'react'
import { createWebSocket } from '../services/websockets'

export default function useWebSocket(onMessage) {

  useEffect(() => {

    const socket = createWebSocket(onMessage)

    return () => {
      socket.close()
    }

  }, [])
}
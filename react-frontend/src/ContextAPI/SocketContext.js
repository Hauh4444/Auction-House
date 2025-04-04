// External Libraries
import { createContext, useContext } from 'react';

// Create the SocketContext
export const SocketContext = createContext(null);

// Custom hook to access socket context
export const useSocket = () => useContext(SocketContext);
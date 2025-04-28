// External Libraries
import { createContext, useContext } from "react";

// Create the web vitals context
export const WebVitalsContext = createContext(null);

// Custom hook to access web vitals context
export const useWebVitals = () => useContext(WebVitalsContext);
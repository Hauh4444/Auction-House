// External Libraries
import { createContext, useContext } from "react";

// Create the cart context
export const CartContext = createContext(null);

// Custom hook to access cart context
export const useCart = () => useContext(CartContext);
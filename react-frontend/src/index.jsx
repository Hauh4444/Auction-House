// External Libraries
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

// Internal Modules
import CartProvider from "@/ContextAPI/CartProvider";
import App from "@/App";

// Stylesheets
import "./index.scss";

/**
 * Entry Point of the Application
 *
 * This file serves as the main entry point for the React application. It sets up the root rendering of
 * the app, wrapping it in `StrictMode` for detecting potential problems and `BrowserRouter`
 * for enabling client-side routing.
 *
 * Features:
 * - Renders the root React component using `createRoot` from `react-dom/client`.
 * - Utilizes `StrictMode` to highlight potential issues in the application.
 * - Employs `BrowserRouter` to facilitate client-side routing within the app.
 */
createRoot(document.getElementById("root")).render(
    <StrictMode>
        <BrowserRouter>
            <CartProvider>
                <App />
            </CartProvider>
        </BrowserRouter>
    </StrictMode>
);

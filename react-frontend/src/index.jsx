// External Libraries
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import posthog from "posthog-js"; // Importing PostHog for analytics

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
 * for enabling client-side routing. It also initializes PostHog for analytics tracking.
 *
 * Features:
 * - Renders the root React component using `createRoot` from `react-dom/client`.
 * - Utilizes `StrictMode` to highlight potential issues in the application.
 * - Employs `BrowserRouter` to facilitate client-side routing within the app.
 * - Initializes PostHog for user interaction analytics tracking.
 */

// Initialize PostHog
posthog.init("YOUR_POSTHOG_API_KEY", { api_host: "https://app.posthog.com" });

/**
 * Tracking the page view for PostHog when the app loads.
 */
posthog.capture('App Loaded', {
  path: window.location.pathname, // Track the initial page load
});

// Render the app
createRoot(document.getElementById("root")).render(
    <StrictMode>
        <BrowserRouter>
            <CartProvider>
                <App /> {/* Main App component */}
            </CartProvider>
        </BrowserRouter>
    </StrictMode>
);

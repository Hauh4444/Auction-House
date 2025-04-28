// External Libraries
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import posthog from "posthog-js";
import { PostHogProvider } from 'posthog-js/react';

// Internal Modules
import CartProvider from "@/ContextAPI/CartProvider";
import WebVitalsProvider from "@/ContextAPI/WebVitalsProvider";
import App from "@/App";

// Stylesheets
import "./index.scss";

posthog.init(
    import.meta.env.VITE_PUBLIC_POSTHOG_KEY,
    {
        api_host: import.meta.env.VITE_PUBLIC_POSTHOG_HOST,
        autocapture: true,
        capture_pageleave: true,
        mask_all_text: true,
        mask_text_selectors: ['input[type="password"]', 'input[type="email"]'],
        session_recording: {
            recordCanvas: true,
        }
    }
);

posthog.startSessionRecording();

/**
 * Entry Point of the Application
 *
 * This file serves as the main entry point for the React application. It sets up the root rendering of
 * the app, wrapping it in `StrictMode` for detecting potential problems, `PostHogProvider` to handle web
 * analytics, and `BrowserRouter` for enabling client-side routing.
 *
 * Features:
 * - Renders the root React component using `createRoot` from `react-dom/client`.
 * - Utilizes `StrictMode` to highlight potential issues in the application.
 * - Uses `PostHogProvider` to handle web analytics of the application.
 * - Employs `BrowserRouter` to facilitate client-side routing within the application.
 */
createRoot(document.getElementById("root")).render(
    <StrictMode>
        <PostHogProvider client={ posthog }>
            <BrowserRouter>
                <CartProvider>
                    <WebVitalsProvider>
                        <App />
                    </WebVitalsProvider>
                </CartProvider>
            </BrowserRouter>
        </PostHogProvider>
    </StrictMode>
);

// External Libraries
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

// Internal Modules
import App from "@/App";

// Stylesheets
import "./index.scss";

// Render the root of the React app, wrapped in StrictMode and BrowserRouter
// StrictMode helps identify potential problems in the app, and BrowserRouter enables client-side routing.
createRoot(document.getElementById("root")).render(
    <StrictMode>
        <BrowserRouter>
            <App /> {/* Main App component */}
        </BrowserRouter>
    </StrictMode>
);

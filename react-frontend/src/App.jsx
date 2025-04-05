// External Libraries
import { useEffect, useState } from  "react";
import { createTheme, ThemeProvider } from  "@mui/material/styles";

// Internal Modules
import PublicRoutes from "@/Routes/PublicRoutes";

// Stylesheets
import "./App.scss";

// Theme configurations for dark and light modes
const darkTheme = createTheme({
    palette: {
        mode: "dark", // Dark theme
    },
});

const lightTheme = createTheme({
    palette: {
        mode: "light", // Light theme
    },
});

/**
 * App Component
 *
 * This component serves as the root of the application, managing the theme mode (dark or light)
 * and rendering the public routes of the app.
 *
 * Features:
 * - Determines the user's system preference for dark mode and applies the appropriate theme.
 * - Listens for changes in the system's color scheme preference to update the theme dynamically.
 *
 * @returns {JSX.Element}
 * - Renders the `ThemeProvider` with the selected theme (light theme currently).
 * - Contains the `PublicRoutes` component, which defines the application"s routing for public pages.
 */
function App() {
    // State to manage the theme mode (dark or light)
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        // Check the user's system preference for dark mode
        const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
        setIsDarkMode(prefersDarkMode);

        // Media query listener to track changes in the system's color scheme preference
        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
        const changeListener = (e) => setIsDarkMode(e.matches);

        // Add the listener and clean it up when the component is unmounted
        mediaQuery.addEventListener("change", changeListener);
        return () => mediaQuery.removeEventListener("change", changeListener);
    }, []); 

    // Apply the light theme regardless of user preference for now
    // Will need to replace lightTheme with 'isDarkMode ? darkTheme : lightTheme'
    return (
        <ThemeProvider theme={lightTheme}>
            {/* Public routes of the app */}
            <PublicRoutes />
        </ThemeProvider>
    );
}

export default App;

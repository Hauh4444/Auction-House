// External Libraries
import { useEffect, useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
// Internal Modules
import PublicRoutes from "@/Routes/PublicRoutes";
// Stylesheets
import "./App.scss";


const darkTheme = createTheme({
    palette: {
        mode: "dark",  // Dark mode palette
    },
});

const lightTheme = createTheme({
    palette: {
        mode: "light",  // Light mode palette
    },
});

function App() {
    // State hook to manage whether dark mode is enabled or not
    const [isDarkMode, setIsDarkMode] = useState(false);

    // useEffect hook runs on component mount and handles detecting system theme preference
    useEffect(() => {
        // Check the system's color scheme preference for dark mode
        const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
        setIsDarkMode(prefersDarkMode);  // Set the initial state based on the system preference

        // Listen for any changes to the system color scheme (dark/light mode)
        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
        const changeListener = (e) => setIsDarkMode(e.matches);  // Update the state when preference changes

        // Add event listener for color scheme changes
        mediaQuery.addEventListener("change", changeListener);

        // Cleanup function to remove the event listener when the component unmounts
        return () => mediaQuery.removeEventListener("change", changeListener);
    }, []);  // Empty dependency array means this effect runs only once after the initial render

    // Currently, the theme is hardcoded as lightTheme.
    // This should be updated based on `isDarkMode`-> isDarkMode ? darkTheme : lightTheme
    return (
        <ThemeProvider theme={lightTheme}>
            <PublicRoutes />
        </ThemeProvider>
    );
}

export default App;

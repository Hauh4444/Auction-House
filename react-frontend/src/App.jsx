// External Libraries
import { useEffect, useState } from  "react";
import { createTheme, ThemeProvider } from  "@mui/material/styles";
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
        mode: "light",
    },
});

function App() {
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
        setIsDarkMode(prefersDarkMode);

        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
        const changeListener = (e) => setIsDarkMode(e.matches);

        mediaQuery.addEventListener("change", changeListener);

        return () => mediaQuery.removeEventListener("change", changeListener);
    }, []);

    return (
        <ThemeProvider theme={lightTheme}>
            <PublicRoutes/>
        </ThemeProvider>
    );
}

export default App;

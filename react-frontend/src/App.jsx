import PublicRoutes from "@/Routes/PublicRoutes";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import "./App.scss";

const darkTheme = createTheme({
    palette: {
        mode: "dark",
    },
})
const lightTheme = createTheme({
    palette: {
        mode: "light",
    },
})

function App() {
    return (
        <>
            <ThemeProvider theme={darkTheme}>
                <PublicRoutes />
            </ThemeProvider>
        </>
  )
};

export default App;

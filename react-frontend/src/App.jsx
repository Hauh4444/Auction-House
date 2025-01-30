import PublicRoutes from './Routes/PublicRoutes';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import './App.scss';

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    }
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

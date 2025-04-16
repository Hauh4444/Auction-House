// External Libraries
import { useEffect, useState } from "react";
import { FaArrowLeft } from "react-icons/fa";
import { FormControl, Button, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./SystemLogs.scss";

const SystemLogs = () => {
    const [logs, setLogs] = useState([]);
    const [currentLog, setCurrentLog] = useState("");
    const [logData, setLogData] = useState([]);
    const [level, setLevel] = useState("ALL");
    const [date, setDate] = useState(null);

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/logs/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => setLogs(res.data.logs))
            .catch(err => console.error(err)); // Log errors if any
    }, []);

    const getLog = (log, level, selectedDate = date) => {
        setLevel(level);

        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/logs/${ log }/`,
            {
                params: {
                    level: level !== "ALL" ? level : null,
                    date: selectedDate ? dayjs(selectedDate).format("YYYY-MM-DD") : null,
                },
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then((res) => setLogData(res.data.log))
            .catch(() => setLogData(null));
    };

    const selectLog = (log) => {
        setCurrentLog(log);
        getLog(log, level);
    };

    return (
        <div className="systemLogsPage page">
            <div className="mainPage">
                <Header />

                <h1>System Logs</h1>
                
                <div className="content">
                    {!currentLog ? (
                        <div className="logs">
                            {logs.map((log, index) => (
                                <div className="log" key={index}>
                                    <Button
                                        className="btn"
                                        onClick={ () => selectLog(log) }
                                    >
                                        { log }
                                    </Button>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <>
                            <div className="filters">
                                <Button
                                    className="backBtn"
                                    onClick={ () => { setCurrentLog("") } }
                                >
                                    <FaArrowLeft />
                                </Button>
                                <FormControl size="small">
                                    <InputLabel id="levelLabel">Level</InputLabel>
                                    <Select
                                        className="levelSelect"
                                        labelId="levelLabel"
                                        label="Level"
                                        name="level"
                                        variant="outlined"
                                        value={ level }
                                        onChange={ (e) => getLog(currentLog, e.target.value) }
                                    >
                                        <MenuItem value={ "ALL" }>All</MenuItem>
                                        <MenuItem value={ "DEBUG" }>Debug</MenuItem>
                                        <MenuItem value={ "INFO" }>Info</MenuItem>
                                        <MenuItem value={ "WARNING" }>Warning</MenuItem>
                                        <MenuItem value={ "ERROR" }>Error</MenuItem>
                                        <MenuItem value={ "CRITICAL" }>Critical</MenuItem>
                                    </Select>
                                </FormControl>

                                <LocalizationProvider dateAdapter={ AdapterDayjs }>
                                    <DatePicker
                                        label="Filter by Date"
                                        value={ date }
                                        onChange={(newValue) => {
                                            setDate(newValue);
                                            getLog(currentLog, level, newValue);
                                        }}
                                        renderInput={ (params) => <TextField { ...params } size="small" /> }
                                    />
                                </LocalizationProvider>
                            </div>

                            <div className="logData">
                                {logData.map((line, index) => (
                                    <div key={ index }>{ line }</div>
                                ))}
                            </div>
                        </>
                    )}
                </div>
            </div>
            <RightNav />
        </div>
    );
}

export default SystemLogs;
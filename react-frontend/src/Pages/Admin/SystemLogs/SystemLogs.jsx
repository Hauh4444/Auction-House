// External Libraries
import { useState } from "react";
import { FormControl, Button, InputLabel, MenuItem, Select } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./SystemLogs.scss";

const SystemLogs = () => {
    const [currentLog, setCurrentLog] = useState("");
    const [logData, setLogData] = useState([]);

    const logs = ["admin"];

    const handleSubmit = () => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/logs/${ currentLog }/`, {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
        })
            .then((res) => {
                setLogData(res.data.log);
            })
            .catch(() => setLogData(null));
    };

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text).then(() => {
            alert("Copied to clipboard: " + text);
        });
    };

    return (
        <div className="systemLogsPage page">
            <div className="mainPage">
                <Header />

                <h1>System Logs</h1>
                
                <div className="content">
                    <div className="filters">
                        <FormControl>
                            <InputLabel id="logLabel">Log</InputLabel>
                            <Select
                                id="logInput"
                                labelId="logLabel"
                                aria-labelledby="logLabel"
                                className="logInput"
                                value={ currentLog }
                                onChange={ (e) => setCurrentLog(e.target.value) }
                                variant="outlined"
                            >
                                {logs.map((filterLog, index) => (
                                    <MenuItem value={ filterLog } key={ index }>
                                        { filterLog.charAt(0).toUpperCase() + filterLog.slice(1) }
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                        <Button className="submitBtn" onClick={ handleSubmit }>Submit</Button>
                    </div>
                    {logData && (
                        <div className="log">
                            {logData.map((line, index) => (
                                <div key={index}>{line}</div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
            <RightNav />
        </div>
    );
}

export default SystemLogs;
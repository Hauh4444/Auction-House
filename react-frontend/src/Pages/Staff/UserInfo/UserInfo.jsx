// External Libraries
import { useState } from "react";
import { FormControl, Button, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./UserInfo.scss";

const UserInfo = () => {
    const [currentRoute, setCurrentRoute] = useState("user");
    const [userIdInput, setUserIdInput] = useState("");
    const [userData, setUserData] = useState(null);

    const routes = ["user", "profile", "orders", "listings", "transactions", "deliveries", "reviews"];

    const handleSubmit = () => {
        let apiRoute = currentRoute;
        if (apiRoute === "user") { apiRoute = ""; }

        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/${ apiRoute }/`, {
            params: { user_id: userIdInput },
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
        })
            .then((res) => {
                setUserData(res.data[currentRoute]);
            })
            .catch(() => setUserData([]));
    };

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text).then(() => {
            alert("Copied to clipboard: " + text);
        });
    };

    return (
        <div className="userInfoPage page">
            <div className="mainPage">
                <Header />

                <h1>User Info</h1>
                <div className="content">
                    <div className="filters">
                        <FormControl>
                            <InputLabel id="routeLabel">Info</InputLabel>
                            <Select
                                id="routeInput"
                                labelId="routeLabel"
                                aria-labelledby="routeLabel"
                                className="routeInput"
                                value={ currentRoute }
                                onChange={ (e) => setCurrentRoute(e.target.value) }
                                variant="outlined"
                            >
                                {routes.map((filterRoute, index) => (
                                    <MenuItem value={ filterRoute } key={ index }>
                                        { filterRoute.charAt(0).toUpperCase() + filterRoute.slice(1) }
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                        <TextField
                            className="input"
                            value={ userIdInput }
                            label="User ID"
                            type="text"
                            onChange={ (e) => setUserIdInput(e.target.value) }
                            variant="outlined"
                        />
                        <Button className="submitBtn" onClick={ handleSubmit }>Submit</Button>
                    </div>
                    <table className="data">
                        {Array.isArray(userData) && userData.length > 0 ? (
                            <>
                                <thead>
                                <tr className="header">
                                    {Object.keys(userData[0]).map((key, index) => (
                                        <th key={ index }>{ key }</th>
                                    ))}
                                </tr>
                                </thead>
                                <tbody>
                                {userData.map((item, rowIndex) => (
                                    <tr className="item" key={ rowIndex }>
                                        {Object.keys(item).map((key, colIndex) => (
                                            <td
                                                key={ colIndex }
                                                onClick={ () => handleCopy(item[key]) }
                                                style={ { cursor: "pointer", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }
                                                title={ item[key] }
                                            >
                                                { item[key] }
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                                </tbody>
                            </>
                        ) : (
                            userData && (
                                <>
                                    <thead>
                                    <tr className="header">
                                        {Object.keys(userData).map((key, index) => (
                                            <th key={ index }>{ key }</th>
                                        ))}
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr className="item">
                                        {Object.keys(userData).map((key, index) => (
                                            <td
                                                key={ index }
                                                onClick={ () => handleCopy(userData[key]) }
                                                style={ { cursor: "pointer", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }
                                                title={ userData[key] }
                                            >
                                                { userData[key] }
                                            </td>
                                        ))}
                                    </tr>
                                    </tbody>
                                </>
                            )
                        )}
                    </table>
                </div>
            </div>
            <RightNav />
        </div>
    );
};

export default UserInfo;
// External Libraries
import { useState } from "react";
import { FormControl, Button, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext.js";

// Stylesheets
import "./ManageUsers.scss";

const ManageUsers = () => {
    const auth = useAuth();

    const [currentRoute, setCurrentRoute] = useState("user");
    const [userIdInput, setUserIdInput] = useState("");
    const [userData, setUserData] = useState(null);
    const [edit, setEdit] = useState(false);

    const routes = ["user", "profile", "orders", "listings", "transactions", "deliveries", "reviews"];
    const ids = ["user_id", "profile_id", "order_id", "listing_id", "transaction_id", "delivery_id", "review_id"];

    const handleSubmit = () => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/${ currentRoute !== "user" ? currentRoute : "" }/`,
            {
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

    const handleChangeMode = (bool, item) => {
        setEdit(bool);
        if (bool) return;
        let id = item[ids[currentRoute.findIndex(route => route === currentRoute)]];
        axios.update(`${ import.meta.env.VITE_BACKEND_API_URL }/user/${ currentRoute !== "user" ? currentRoute : "" }/${ id }`,
            {

            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => handleSubmit())
            .catch((err) => console.error(err));
    }

    const handleEdit = (key, val) => {
        let data = userData;
        data[key] = val;
        setUserData(data);
    }

    const handleDelete = (item) => {
        let id = item[ids[currentRoute.findIndex(route => route === currentRoute)]];
        axios.delete(`${ import.meta.env.VITE_BACKEND_API_URL }/user/${ currentRoute !== "user" ? currentRoute : "" }/${ id }`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => handleSubmit())
            .catch((err) => console.error(err));
    }

    return (
        <div className="userInfoPage page">
            <div className="mainPage">
                <Header />

                <h1>Users</h1>
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
                                    <>
                                        <tr className="item" key={ rowIndex }>
                                            {Object.keys(item).map((key, colIndex) => (
                                                <td
                                                    key={ colIndex }
                                                    onClick={ () => handleCopy(item[key]) }
                                                    style={ { cursor: "pointer", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }
                                                >
                                                    {edit ? (
                                                        <TextField
                                                            className="input"
                                                            value={ item[key] !== null ? String(item[key]) : "" }
                                                            label=""
                                                            type="text"
                                                            onChange={ (e) => handleEdit(key, e.target.value) }
                                                            variant="outlined"
                                                        />
                                                    ) : (
                                                        item[key] !== null ? String(item[key]) : ""
                                                    )}
                                                </td>
                                            ))}
                                        </tr>
                                        {auth.user.role === "admin" && (
                                            <>
                                                <Button className="btn" onClick={ () => handleChangeMode(!edit, item) }>{ edit ? "Edit" : "Submit" }</Button>
                                                <Button className="btn" onClick={ () => handleDelete(item) }>Delete</Button>
                                            </>
                                        )}
                                    </>
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
                                            >
                                                {edit ? (
                                                    <TextField
                                                        className="input"
                                                        value={ userData[key] !== null ? String(userData[key]) : "" }
                                                        label=""
                                                        type="text"
                                                        onChange={ (e) => handleEdit(key, e.target.value) }
                                                        variant="outlined"
                                                    />
                                                ) : (
                                                    userData[key] !== null ? String(userData[key]) : ""
                                                )}
                                            </td>
                                        ))}
                                        {auth.user.role === "admin" && (
                                            <>
                                                <Button className="btn" onClick={ () => handleChangeMode(!edit, userData) }>{ edit ? "Edit" : "Submit" }</Button>
                                                <Button className="btn" onClick={ () => handleDelete(userData) }>Delete</Button>
                                            </>
                                        )}
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

export default ManageUsers;
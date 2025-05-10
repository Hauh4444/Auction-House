// External Libraries
import { useState } from "react";
import { FaEdit, FaCheck } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { FormControl, Button, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext";

// Stylesheets
import "./ManageUsers.scss";

const ManageUsers = () => {
    const auth = useAuth(); // Fetch the authentication context

    const [ currentRoute, setCurrentRoute ] = useState("user");
    const [ userIdInput, setUserIdInput ] = useState("");
    const [ userData, setUserData ] = useState(null);
    const [ editingRow, setEditingRow ] = useState(null);

    const routes = [ "user", "profile", "orders", "listings", "transactions", "deliveries", "reviews" ];
    const ids = [ "user_id", "profile_id", "order_id", "listing_id", "transaction_id", "delivery_id", "review_id" ];

    const handleSubmit = () => {
        axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/user/${currentRoute !== "user" ? currentRoute + "/" : ""}`, {
            params: { user_id: userIdInput },
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
        })
            .then((res) => {
                setUserData(res.data[currentRoute]);
                setEditingRow(null);
            })
            .catch(() => setUserData([]));
    };

    const handleCopy = (text, rowIndex) => {
        if (editingRow === rowIndex) return;
        navigator.clipboard.writeText(text).then(() => {
            alert("Copied to clipboard: " + text);
        });
    };

    const handleChangeMode = (rowId, item) => {
        if (editingRow === rowId) {
            let id = item[ids[routes.findIndex(route => route === currentRoute)]];
            axios.put(`${import.meta.env.VITE_BACKEND_API_URL}/user/${currentRoute !== "user" ? currentRoute + "/" : ""}${id}/`, item, {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
                .then(() => {
                    handleSubmit();
                })
                .catch((err) => console.error(err));
        } else {
            setEditingRow(rowId);
        }
    };

    const handleEdit = (key, val, index) => {
        const updatedData = Array.isArray(userData) ? [ ...userData ] : { ...userData };
        if (Array.isArray(updatedData)) {
            updatedData[index][key] = val;
        } else {
            updatedData[key] = val;
        }
        setUserData(updatedData);
    };

    const handleDelete = (item) => {
        let id = item[ids[routes.findIndex(route => route === currentRoute)]];
        axios.delete(`${import.meta.env.VITE_BACKEND_API_URL}/user/${currentRoute !== "user" ? currentRoute + "/" : ""}${id}/`, {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
        })
            .then(() => handleSubmit())
            .catch((err) => console.error(err));
    };

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
                                label="Info"
                                value={ currentRoute }
                                onChange={ (e) => setCurrentRoute(e.target.value) }
                                variant="outlined"
                                className="routeInput"
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
                            onChange={ (e) => setUserIdInput(e.target.value) }
                            onKeyDown={ (e) => { if (e.key === "Enter") handleSubmit() } }
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
                                    {auth.user.role === "admin" && (
                                        <>
                                            <th>Edit</th>
                                            <th>Delete</th>
                                        </>
                                    )}
                                </tr>
                                </thead>
                                <tbody>
                                {userData && userData.map((item, rowIndex) => (
                                    <tr className="item" key={ rowIndex }>
                                        {Object.keys(item).map((key, colIndex) => (
                                            <td
                                                key={ colIndex }
                                                onClick={ () => handleCopy(item[key], rowIndex) }
                                                style={{ cursor: editingRow === rowIndex ? "default" : "pointer", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}
                                            >
                                                {editingRow === rowIndex ? (
                                                    <TextField
                                                        className="input"
                                                        value={ item[key] !== null ? String(item[key]) : "" }
                                                        onChange={ (e) => handleEdit(key, e.target.value, rowIndex) }
                                                        variant="outlined"
                                                    />
                                                ) : (
                                                    item[key] !== null ? String(item[key]) : ""
                                                )}
                                            </td>
                                        ))}
                                        {auth.user.role === "admin" && (
                                            <>
                                                <td className="btnCell">
                                                    <Button className="btn" onClick={ () => handleChangeMode(rowIndex, item) }>
                                                        {editingRow === rowIndex ? <FaCheck /> : <FaEdit />}
                                                    </Button>
                                                </td>
                                                <td className="btnCell">
                                                    <Button className="btn" onClick={ () => handleDelete(item) }>
                                                        <MdDelete />
                                                    </Button>
                                                </td>
                                            </>
                                        )}
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
                                        {auth.user.role === "admin" && (
                                            <>
                                                <th>Edit</th>
                                                <th>Delete</th>
                                            </>
                                        )}
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr className="item">
                                        {Object.keys(userData).map((key, index) => (
                                            <td
                                                key={ index }
                                                onClick={ () => handleCopy(userData[key], 0) }
                                                style={{ cursor: editingRow === 0 ? "default" : "pointer", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}
                                            >
                                                {editingRow === 0 ? (
                                                    <TextField
                                                        className="input"
                                                        value={ userData[key] !== null ? String(userData[key]) : "" }
                                                        onChange={ (e) => handleEdit(key, e.target.value, 0) }
                                                        variant="outlined"
                                                    />
                                                ) : (
                                                    userData[key] !== null ? String(userData[key]) : ""
                                                )}
                                            </td>
                                        ))}
                                        {auth.user.role === "admin" && (
                                            <>
                                                <td className="btnCell">
                                                    <Button className="btn" onClick={ () => handleChangeMode(0, userData) }>
                                                        {editingRow === 0 ? <FaCheck /> : <FaEdit />}
                                                    </Button>
                                                </td>
                                                <td className="btnCell">
                                                    <Button className="btn" onClick={ () => handleDelete(userData) }>
                                                        <MdDelete />
                                                    </Button>
                                                </td>
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

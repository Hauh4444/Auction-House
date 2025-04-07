// External Libraries
import { useState } from "react";
import axios from "axios";
import PropTypes from "prop-types";

// Internal Modules
import { AuthContext } from "./AuthContext";

axios.defaults.withCredentials = true;
axios.defaults.headers["Content-Type"] = "application/json";

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState("");

    const checkAuthStatus = async () => {
        try {
            const res = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/auth/auth_status/`);
            setUser(res.data.authenticated ? {"user_id": res.data.id, "role": res.data.role} : null);
        } catch (err) {
            console.log(err);
            setUser(null);
        }
    };

    const login = async (credentials) => {
        try {
            await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/auth/login/`, credentials);
            await checkAuthStatus();
            return true;
        } catch (err) {
            console.log(err);
            setError("Login failed. Please check your credentials.");
            return false;
        }
    };

    const createAccount = async (credentials) => {
        try {
            await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/auth/register/`, credentials);
            await login(credentials);
            return true;
        } catch (err) {
            console.log(err);
            setError("Failed to create account.");
            return false;
        }
    };

    const logout = async () => {
        try {
            await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/auth/logout/`);
            setUser(null);
        } catch (err) {
            console.log(err);
            setError("Logout failed. Please try again.");
        }
    };

    return (
        <AuthContext.Provider value={{ user, error, createAccount, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

AuthProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

export default AuthProvider;

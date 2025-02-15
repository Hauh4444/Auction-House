// External Libraries
import { createContext, useState, useCallback, useContext } from "react";
import axios from "axios";
import PropTypes from "prop-types";


const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const checkAuthStatus = useCallback(async () => {
        axios.get("http://127.0.0.1:5000/api/auth_status", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
            .then(res => {
                if (res.data.isAuthenticated) {
                    setUser(res.data.user);
                } else {
                    setUser(null);
                }
            })
            .catch(err => {
                console.log(err);
                setUser(null);
            });
    }, []);

    const createAccount = useCallback((credentials) => {
        axios.post("http://127.0.0.1:5000/api/register", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
            data: credentials,
        })
            .then(() => checkAuthStatus())
            .catch(err => console.log(err));
    }, [checkAuthStatus]);

    const login = useCallback((credentials) => {
        axios.post("http://127.0.0.1:5000/api/login", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
            data: credentials,
        })
            .then(() => checkAuthStatus())
            .catch(err => console.log(err));
    }, [checkAuthStatus]);

    const logout = useCallback(() => {
        axios.post("http://127.0.0.1:5000/api/logout", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
            .then(() => setUser(null))
            .catch(err => console.log(err));
    }, []);

    return (
        <AuthContext.Provider value={{ user, createAccount, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

AuthProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

export default AuthProvider;
export const useAuth = () => {
    return useContext(AuthContext);
}
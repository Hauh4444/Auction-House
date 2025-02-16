// External Libraries
import { createContext, useState, useCallback, useContext } from "react";
import axios from "axios";
import PropTypes from "prop-types";

// Create the context to hold the authentication state
const AuthContext = createContext(null);

/**
 * AuthProvider Component
 *
 * Provides authentication-related methods and state to the rest of the application.
 * This includes methods to check the authentication status, create an account, login, and logout.
 * The context will be used to share the user information and authentication methods across components.
 *
 * @param {Object} children - The child components that will have access to the authentication context.
 * @returns {JSX.Element} The AuthContext.Provider with authentication methods and state.
 */
const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // State to store the current user

    // Function to check if the user is authenticated
    const checkAuthStatus = useCallback(async () => {
        axios.get("http://127.0.0.1:5000/api/auth_status", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => {
                if (res.data.isAuthenticated) {
                    setUser(res.data.user); // Set the user state if authenticated
                } else {
                    setUser(null); // Clear user state if not authenticated
                }
            })
            .catch(err => {
                console.log(err); // Log errors if any
                setUser(null); // Clear user state on error
            });
    }, []);

    // Function to create a new user account
    const createAccount = useCallback((credentials) => {
        axios.post("http://127.0.0.1:5000/api/register", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
            data: credentials, // Send user credentials to the backend
        })
            .then(() => checkAuthStatus()) // Check authentication status after account creation
            .catch(err => console.log(err)); // Log errors if any
    }, [checkAuthStatus]);

    // Function to log in an existing user
    const login = useCallback((credentials) => {
        axios.post("http://127.0.0.1:5000/api/login", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
            data: credentials, // Send login credentials to the backend
        })
            .then(() => checkAuthStatus()) // Check authentication status after login
            .catch(err => console.log(err)); // Log errors if any
    }, [checkAuthStatus]);

    // Function to log out the current user
    const logout = useCallback(() => {
        axios.post("http://127.0.0.1:5000/api/logout", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(() => setUser(null)) // Clear the user state on logout
            .catch(err => console.log(err)); // Log errors if any
    }, []);

    return (
        // Provide the auth context to the rest of the app
        <AuthContext.Provider value={{ user, createAccount, login, logout }}>
            {children} {/* Render the child components */}
        </AuthContext.Provider>
    );
};

// Define prop types for the AuthProvider component
AuthProvider.propTypes = {
    children: PropTypes.node.isRequired, // Children should be valid React nodes
};

export default AuthProvider;

// Custom hook to access authentication context
export const useAuth = () => {
    return useContext(AuthContext); // Return the value from AuthContext
};

import { createContext, useState, useCallback, useContext } from "react";
import axios from "axios";
import PropTypes from "prop-types";

axios.defaults.withCredentials = true;
axios.defaults.headers["Content-Type"] = "application/json";

// Create the context to hold the authentication state
const AuthContext = createContext(null);

/**
 * AuthProvider Component
 *
 * Provides authentication methods and state to the application.
 *
 * @param {Object} children - The child components that will have access to the authentication context.
 * @returns {JSX.Element} The AuthContext.Provider containing the user state and authentication methods.
 */
const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // State to store the current user
    const [error, setError] = useState(""); // State for error messages

    // Function to check if the user is authenticated
    const checkAuthStatus = useCallback(async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/api/user/auth_status");
            if (res.data.authenticated) {
                setUser(res.data.user); // Set the user state if authenticated
            } else {
                setUser(null); // Clear user state if not authenticated
            }
        } catch (err) {
            console.log(err);
            setUser(null); // Clear user state on error
        }
    }, []);

    // Function to create a new user account
    const createAccount = useCallback(async (credentials) => {
        try {
            await axios.post("http://127.0.0.1:5000/api/user/register", credentials);
            await checkAuthStatus(); // Check authentication status after account creation
            return true; // Indicate success
        } catch (err) {
            console.log(err);
            setError("Failed to create account.");
            return false; // Indicate failure
        }
    }, [checkAuthStatus]);

    // Function to log in an existing user
    const login = useCallback(async (credentials) => {
        try {
            await axios.post("http://127.0.0.1:5000/api/user/login", credentials);
            await checkAuthStatus(); // Check authentication status after login
            return true; // Indicate success
        } catch (err) {
            console.log(err);
            setError("Login failed. Please check your credentials.");
            return false; // Indicate failure
        }
    }, [checkAuthStatus]);

    // Function to log out the current user
    const logout = useCallback(async () => {
        try {
            await axios.post("http://127.0.0.1:5000/api/user/logout");
            setUser(null); // Clear the user state on logout
        } catch (err) {
            console.log(err);
            setError("Logout failed. Please try again.");
        }
    }, []);

    return (
        // Provide the auth context to the rest of the app
        <AuthContext.Provider value={{ user, error, createAccount, login, logout }}>
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

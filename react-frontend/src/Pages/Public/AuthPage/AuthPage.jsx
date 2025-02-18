// External Libraries
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Card, CardContent, CardHeader } from "@mui/material";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

// Stylesheets
import "./AuthPage.scss";

/**
 * Browse Component
 *
 * This component serves as both a login and registration page, allowing users to:
 * - Login with a username and password.
 * - Create a new account by providing additional details.
 * - Toggle between login and registration views.
 */
const AuthPage = () => {
    // State variables for user input fields
    const [username, setUsername] = useState(""); // Stores username input
    const [password, setPassword] = useState(""); // Stores password input
    const [firstName, setFirstName] = useState(""); // Stores first name input (for registration)
    const [lastName, setLastName] = useState(""); // Stores last name input (for registration)
    const [email, setEmail] = useState(""); // Stores email input (for registration)
    const [confirmPassword, setConfirmPassword] = useState(""); // Stores password confirmation input
    const [passwordError, setPasswordError] = useState(""); // Stores error message if passwords do not match
    const [isLogin, setIsLogin] = useState(true); // Boolean state to toggle between login and registration forms

    const navigate = useNavigate(); // Navigate function for routing
    const auth = useAuth(); // Access authentication functions from the AuthProvider context

    /**
     * Handles the login form submission.
     * - Calls the login function from AuthProvider.
     * - Navigates to the home page if login is successful.
     *
     * @param {Event} e - Form submission event.
     */
    const handleSubmitLogin = (e) => {
        e.preventDefault(); // Prevents default form submission behavior

        // Attempt login authorization
        auth.login({
            username,
            password,
        });

        // Navigate to home page on successful login
        if (auth.user) {
            navigate("/");
        }
    };

    /**
     * Handles the account creation form submission.
     * - Validates that password and confirm password match.
     * - Calls the createAccount function from AuthProvider.
     * - Navigates to the home page if registration is successful.
     *
     * @param {Event} e - Form submission event.
     */
    const handleSubmitCreateAccount = (e) => {
        e.preventDefault(); // Prevents default form submission behavior

        // Check if passwords match
        if (password !== confirmPassword) {
            setPasswordError("Passwords do not match");
            return;
        } else {
            setPasswordError(""); // Clear error if passwords match
        }

        // Attempt create account authorization
        auth.createAccount({
            username,
            firstName,
            lastName,
            email,
            password,
        });

        // Navigate to home page on successful registration
        if (auth.user) {
            navigate("/");
        }
    };

    return (
        <div className="authPage">
            {/* Main container for authentication form */}
            <Card className="card">
                {/* Card header with dynamic title (Login or Create Account) */}
                <CardHeader title={isLogin ? "Login" : "Create Account"} />

                <CardContent className="content">
                    {/* Authentication form */}
                    <form onSubmit={isLogin ? handleSubmitLogin : handleSubmitCreateAccount} className="form">

                        {/* Username Input Field */}
                        <TextField
                            className="input"
                            label="Username"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />

                        {/* Registration-specific input fields (only displayed when creating an account) */}
                        {!isLogin && (
                            <>
                                {/* First Name Input */}
                                <TextField
                                    className="nameInput"
                                    style={{ float: "left" }}
                                    label="First Name"
                                    type="text"
                                    variant="outlined"
                                    fullWidth
                                    value={firstName}
                                    onChange={(e) => setFirstName(e.target.value)}
                                    required
                                />
                                {/* Last Name Input */}
                                <TextField
                                    className="nameInput"
                                    style={{ float: "right" }}
                                    label="Last Name"
                                    type="text"
                                    variant="outlined"
                                    fullWidth
                                    value={lastName}
                                    onChange={(e) => setLastName(e.target.value)}
                                    required
                                />
                                {/* Email Input */}
                                <TextField
                                    className="input"
                                    label="Email"
                                    type="email"
                                    variant="outlined"
                                    fullWidth
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            < />
                        )}

                        {/* Password Input Field */}
                        <TextField
                            className="input"
                            label="Password"
                            type="password"
                            variant="outlined"
                            fullWidth
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />

                        {/* Confirm Password Field (Only for account creation) */}
                        {!isLogin && (
                            <TextField
                                className="input"
                                label="Confirm Password"
                                type="password"
                                variant="outlined"
                                fullWidth
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                            />
                        )}

                        {/* Error message display for password mismatch */}
                        {passwordError && <div className="error-message">{passwordError}</div>}

                        {/* Submit Button (Dynamically labeled based on form mode) */}
                        <Button className="btn" type="submit" variant="contained" color="primary" fullWidth>
                            {isLogin ? "Login" : "Create Account"}
                        </Button>
                    </form>

                    {/* Toggle button for switching between login and registration */}
                    <Button
                        className="toggleBtn"
                        onClick={() => setIsLogin(!isLogin)}
                        variant="text"
                        fullWidth
                    >
                        {isLogin ? "Don't have an account? Create one" : "Already have an account? Login"}
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
};

export default AuthPage;

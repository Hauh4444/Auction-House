// External Libraries
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Card, CardContent, CardHeader } from "@mui/material";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

// Stylesheets
import "./AuthPage.scss"

/**
 * AuthPage Component
 *
 * This component provides a user authentication form that supports both login and
 * account creation. It includes input fields for user credentials and dynamically
 * switches between login and registration modes based on user interaction.
 *
 * Features:
 * - Supports user login with username and password.
 * - Enables account creation with fields for first name, last name, email, and password.
 * - Validates password confirmation during registration.
 * - Utilizes Material-UI components (`TextField`, `Button`, `Card`, `CardContent`, `CardHeader`).
 * - Integrates authentication functions from `AuthProvider` context.
 * - Navigates to the home page upon successful login or registration.
 *
 * @returns {JSX.Element} The rendered authentication page component.
 */
const AuthPage = () => {
    // State variables for user input fields
    const [username, setUsername] = useState(""); // Stores username input
    const [password, setPassword] = useState(""); // Stores password input
    const [firstName, setFirstName] = useState(""); // Stores first name input (for registration)
    const [lastName, setLastName] = useState(""); // Stores last name input (for registration)
    const [email, setEmail] = useState(""); // Stores email input (for registration)
    const [confirmPassword, setConfirmPassword] = useState(""); // Stores password confirmation input
    const [loginError, setLoginError] = useState(""); // Stores error message if passwords do not match
    const [isLogin, setIsLogin] = useState(true); // Boolean state to toggle between login and registration forms

    const navigate = useNavigate(); // Navigate hook for routing
    const auth = useAuth(); // Access authentication functions from the AuthProvider context

    /**
     * Handles the login form submission.
     * - Calls the login function from AuthProvider.
     * - Navigates to the home page if login is successful.
     *
     * @param {Event} e - Form submission event.
     */
    const handleSubmitLogin = async (e) => {
        e.preventDefault(); // Prevents default form submission behavior

        // Attempt login authorization
        const success = await auth.login({
            username,
            password,
        });

        // Navigate to home page on successful login
        if (success) {
            navigate("/"); // Navigate only if login is successful
        } else {
            setLoginError("Incorrect username or password");
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
    const handleSubmitCreateAccount = async (e) => {
        e.preventDefault(); // Prevents default form submission behavior

        // Check if passwords match
        if (password !== confirmPassword) {
            setLoginError("Passwords do not match");
            return;
        } else {
            setLoginError(""); // Clear error if passwords match
        }

        // Attempt create account authorization
        const success = await auth.createAccount({
            username,
            firstName,
            lastName,
            email,
            password,
        });

        // Navigate to home page on successful registration
        if (success) {
            navigate("/"); // Navigate only if account creation is successful
        } else {
            setLoginError("Error creating account");
        }
    };

    return (
        <div className="authPage page">
            <div className="authForm">
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
                            {loginError && <div className="errorMessage">{loginError}</div>}

                            {/* Submit Button (Dynamically labeled based on form mode) */}
                            <Button className="btn" type="submit" variant="contained" color="primary" fullWidth>
                                {isLogin ? "Login" : "Create Account"}
                            </Button>
                        </form>

                        {/* Toggle button for switching between login and registration */}
                        <Button
                            className="toggleBtn"
                            onClick={() => {
                                setIsLogin(!isLogin);
                                setLoginError("");
                            }}
                            variant="text"
                            fullWidth
                        >
                            {isLogin ? "Don't have an account? Create one" : "Already have an account? Login"}
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
};

export default AuthPage;

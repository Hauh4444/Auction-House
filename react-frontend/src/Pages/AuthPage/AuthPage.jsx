// External Libraries
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Card, CardContent, CardHeader } from "@mui/material";
// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";
// Stylesheets
import "./AuthPage.scss";

const AuthPage = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [isLogin, setIsLogin] = useState(true); // Track if the login form is being displayed
    const navigate = useNavigate();
    const auth = useAuth();

    const handleSubmitLogin = (e) => {
        e.preventDefault();

        auth.login({
            username,
            password,
        });

        if (auth.user) {
            navigate("/");
        }
    };

    const handleSubmitCreateAccount = (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            setPasswordError("Passwords do not match");
            return;
        } else {
            setPasswordError(""); // Clear error if passwords match
        }

        auth.createAccount({
            username,
            firstName,
            lastName,
            email,
            password,
        });

        if (auth.user) {
            navigate("/");
        }
    };

    return (
        <div className="authPage">
            <Card className="card">
                <CardHeader title={isLogin ? "Login" : "Create Account"} />
                <CardContent className="content">
                    <form onSubmit={isLogin ? handleSubmitLogin : handleSubmitCreateAccount} className="form">
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
                        {!isLogin && (
                            <>
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
                            </>
                        )}
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
                        {passwordError && <div className="error-message">{passwordError}</div>}
                        <Button className="btn" type="submit" variant="contained" color="primary" fullWidth>
                            {isLogin ? "Login" : "Create Account"}
                        </Button>
                    </form>
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

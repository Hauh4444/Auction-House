// External Libraries
import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { TextField, Button, Card, CardContent, CardHeader } from "@mui/material";
import axios from "axios";

// Stylesheets
import "./PasswordReset.scss";

const PasswordReset = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");

    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [resetError, setResetError] = useState("");

    const handleReset = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            setResetError("Passwords do not match");
            return;
        }

        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/auth/password_reset/`,
            {
                token: token,
                new_password: newPassword,
            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => navigate("/"))
            .catch(err => setResetError(err.response.data.error));
    };

    return (
        <div className="passwordResetPage page">
            <div className="passwordResetForm">
                <Card className="card">
                    { /* Card header with dynamic title (Login or Create Account) */ }
                    <CardHeader title="Reset Password" />

                    <CardContent className="content">
                        { /* Authentication form */ }
                        <form onSubmit={ (e) => handleReset(e) } className="form">
                            { /* Password Input Field */ }
                            <TextField
                                className="input"
                                data-testid="passwordInput"
                                label="Password"
                                type="password"
                                variant="outlined"
                                fullWidth
                                value={ newPassword }
                                onChange={ (e) => setNewPassword(e.target.value) }
                                required
                            />

                            { /* Confirm Password Field */ }
                            <TextField
                                className="input"
                                data-testid="confirmPasswordInput"
                                label="Confirm Password"
                                type="password"
                                variant="outlined"
                                fullWidth
                                value={ confirmPassword }
                                onChange={ (e) => setConfirmPassword(e.target.value) }
                                required
                            />

                            { /* Error message display for password mismatch */ }
                            { resetError && <div className="errorMessage">{ resetError  }</div>}

                            { /* Reset Button */ }
                            <Button className="btn" type="submit" variant="contained" color="primary" fullWidth>
                                Reset
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default PasswordReset;

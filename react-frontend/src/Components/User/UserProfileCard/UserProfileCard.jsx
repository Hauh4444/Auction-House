// External Libraries
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, TextField, Button } from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Stylesheets
import "./UserProfileCard.scss"

const UserProfileCard = () => {
    const [edit, setEdit] = useState(false);
    const [user, setUser] = useState({})

    // Fetch user profile data from the backend API
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/auth_status", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => setUser(res.data)) // Set the user state
            .catch(err => console.log(err)); // Log errors if any
    }, []); // Empty dependency array to ensure it runs only once when the component is mounted

    // On submit, post updated user profile data to the backend API
    const handleSubmit = () => {
        axios.post("http://127.0.0.1:5000/api/update_user_profile", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensure cookies are sent if needed
            data: user,
        })
            .then(() => {setEdit(false)}) // Turn edit mode off if no errors
            .catch(err => console.log(err)); // Log errors if any
    }

    return (
        <Card className="card">
            <CardHeader title="User Profile"></CardHeader>
            <CardContent className="content">
                {!edit ? (
                    /* If edit mode is off, display the data */
                    <>
                        <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
                        <p><strong>Date of Birth:</strong> {user.date_of_birth}</p>
                        <p><strong>Phone Number:</strong> {user.phone_number}</p>
                        <p><strong>Address:</strong> {user.address} {user.city}, {user.state}, {user.country}</p>
                        <p><strong>Bio:</strong> {user.bio}</p>
                        {/* Toggle edit mode button */}
                        <Button className="btn" onClick={() => setEdit(true)}>Edit</Button>
                    </>
                ) : (
                    /* If edit mode is on, display the data as text fields that can be editted and submitted */
                    <>
                        {/* First name field */}
                        <TextField
                            className="input"
                            label="First Name"
                            name="first_name"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={user.first_name}
                            onChange={(e) => setUser({...user, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Last name field */}
                        <TextField
                            className="input"
                            label="Last Name"
                            name="last_name"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={user.last_name}
                            onChange={(e) => setUser({...user, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Date of birth field */}
                        <TextField
                            className="input"
                            label="Date of Birth"
                            name="date_of_birth"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={user.date_of_birth}
                            onChange={(e) => setUser({...user, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Phone number field */}
                        <TextField
                            className="input"
                            label="Phone Number"
                            name="phone_number"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={user.phone_number}
                            onChange={(e) => setUser({...user, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Address field */}
                        <TextField
                            className="input"
                            label="Address"
                            name="address"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={user.address}
                            onChange={(e) => setUser({...user, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Bio field */}
                        <TextField
                            className="input"
                            label="Bio"
                            name="bio"
                            type="text"
                            variant="outlined"
                            fullWidth
                            value={user.bio}
                            onChange={(e) => setUser({...user, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Submit button */}
                        <Button className="btn" onClick={() => handleSubmit(user)}>Submit</Button>
                    </>
                )}
            </CardContent>
        </Card>
    )
}

// Define the expected shape of the user prop
UserProfileCard.propTypes = {
    user: PropTypes.shape({
        first_name: PropTypes.string,
        last_name: PropTypes.string,
        date_of_birth: PropTypes.string,
        phone_number: PropTypes.string,
        address: PropTypes.string,
        city: PropTypes.string,
        state: PropTypes.string,
        country: PropTypes.string,
        bio: PropTypes.string,
    }),
};

export default UserProfileCard;
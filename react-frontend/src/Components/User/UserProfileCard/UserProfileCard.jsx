// External Libraries
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, TextField, Button } from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Stylesheets
import "./UserProfileCard.scss"

/**
 * UserProfileCard Component
 *
 * This component displays a user's profile information and allows the user to edit
 * their details. It fetches user data from a backend API and renders it in a card format.
 * The component supports toggling between viewing and editing modes. In editing mode,
 * users can update their first name, last name, date of birth, phone number, address,
 * and bio. The updated information is submitted back to the backend API for persistence.
 *
 * Features:
 * - Fetches user profile data from an API upon mounting.
 * - Toggles between view and edit modes for user information.
 * - Submits updated user data to the API for saving.
 *
 * @returns {JSX.Element} A card component displaying user profile information
 *                        with the ability to edit and submit updates.
 */
const UserProfileCard = () => {
    const [edit, setEdit] = useState(false);
    const [profile, setProfile] = useState({})

    // Fetch user profile data from the backend API
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/get_user_profile", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => setProfile(res.data)) // Set the user state
            .catch(err => console.log(err)); // Log errors if any
    }, []); // Empty dependency array to ensure it runs only once when the component is mounted

    // On submit, post updated user profile data to the backend API
    const handleSubmit = () => {
        axios.post("http://127.0.0.1:5000/api/update_user_profile", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensure cookies are sent if needed
            data: profile,
        })
            .then(() => {setEdit(false)}) // Turn edit mode off if no errors
            .catch(err => console.log(err)); // Log errors if any
    }

    return (
        <Card className="userProfileCard">
            <CardHeader title="User Profile" sx={{width: "fit-content", margin: "0 auto"}}></CardHeader>
            <CardContent className="content">
                {!edit ? (
                    /* If edit mode is off, display the data */
                    <>
                        <div className="profileInfo">
                            <p><strong>Name:</strong> {profile.first_name} {profile.last_name}</p>
                            <p><strong>Date of Birth:</strong> {profile.date_of_birth}</p>
                            <p><strong>Phone Number:</strong> {profile.phone_number}</p>
                            <p><strong>Address:</strong> {profile.address}</p>
                            <p><strong>City:</strong> {profile.city}</p>
                            <p><strong>State:</strong> {profile.state}</p>
                            <p><strong>Country:</strong> {profile.country}</p>
                        </div>
                        {/*<img src={`data:image/jpg;base64,${profile.profile_picture}`} alt="" />*/}
                        <p className="bio"><strong>Bio:</strong> {profile.bio}</p>
                        {/* Toggle edit mode button */}
                        <Button className="btn" onClick={() => setEdit(true)}>Edit</Button>
                    </>
                ) : (
                    /* If edit mode is on, display the data as text fields that can be editted and submitted */
                    <>
                        {/* First name field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "left" }}
                            label="First Name"
                            name="first_name"
                            type="text"
                            variant="outlined"
                            value={profile.first_name}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Last name field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "right" }}
                            label="Last Name"
                            name="last_name"
                            type="text"
                            variant="outlined"
                            value={profile.last_name}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Date of birth field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "left" }}
                            label="Date of Birth"
                            name="date_of_birth"
                            type="text"
                            variant="outlined"
                            value={profile.date_of_birth}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Phone number field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "right" }}
                            label="Phone Number"
                            name="phone_number"
                            type="text"
                            variant="outlined"
                            value={profile.phone_number}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Address field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "left" }}
                            label="Address"
                            name="address"
                            type="text"
                            variant="outlined"
                            value={profile.address}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* City field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "right" }}
                            label="City"
                            name="city"
                            type="text"
                            variant="outlined"
                            value={profile.city}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* State field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "left" }}
                            label="State"
                            name="state"
                            type="text"
                            variant="outlined"
                            value={profile.state}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Country field */}
                        <TextField
                            className="input shortField"
                            style={{ float: "right" }}
                            label="Country"
                            name="country"
                            type="text"
                            variant="outlined"
                            value={profile.country}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Bio field */}
                        <TextField
                            className="input bio"
                            label="Bio"
                            name="bio"
                            type="text"
                            variant="outlined"
                            multiline
                            rows={5}
                            maxrows={10}
                            fullWidth
                            value={profile.bio}
                            onChange={(e) => setProfile({...profile, [e.target.name]: e.target.value})}
                            required
                        />
                        {/* Submit button */}
                        <Button className="btn" onClick={() => handleSubmit(profile)}>Submit</Button>
                    </>
                )}
            </CardContent>
        </Card>
    )
}

// Define the expected shape of the profile prop
UserProfileCard.propTypes = {
    profile: PropTypes.shape({
        first_name: PropTypes.string,
        last_name: PropTypes.string,
        date_of_birth: PropTypes.string,
        phone_number: PropTypes.string,
        address: PropTypes.string,
        city: PropTypes.string,
        state: PropTypes.string,
        country: PropTypes.string,
        profile_picture: PropTypes.string,
        bio: PropTypes.string,
    }),
};

export default UserProfileCard;
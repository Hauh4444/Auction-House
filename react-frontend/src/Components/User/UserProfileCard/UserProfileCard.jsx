// External Libraries
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, TextField, Button } from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

// Stylesheets
import "./UserProfileCard.scss";

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
    const [newProfilePicture, setNewProfilePicture] = useState(""); // For storing the new image

    const auth = useAuth(); // Access authentication functions from the AuthProvider context

    const fields = [
        { label: "First Name", name: "first_name", type: "text", value: profile.first_name },
        { label: "Last Name", name: "last_name", type: "text", value: profile.last_name },
        { label: "Date of Birth", name: "date_of_birth", type: "text", value: profile.date_of_birth },
        { label: "Phone Number", name: "phone_number", type: "text", value: profile.phone_number },
        { label: "Address", name: "address", type: "text", style: { float: "left" }, value: profile.address },
        { label: "City", name: "city", type: "text", style: { float: "right" }, value: profile.city },
        { label: "State", name: "state", type: "text", style: { float: "left" }, value: profile.state },
        { label: "Country", name: "country", type: "text", style: { float: "right" }, value: profile.country },
        { label: "Bio", name: "bio", type: "text", multiline: true, rows: 5, maxrows: 10, fullWidth: true, value: profile.bio },
    ];

    // Fetch user profile data from the backend API
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/profile/" + auth.user, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => setProfile(res.data)) // Set the user state
            .catch(err => console.log(err)); // Log errors if any
    }, []); // Empty dependency array to ensure it runs only once when the component is mounted

    const encodeImageToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onloadend = () => {
                // The result is the base64 encoded string
                const base64String = reader.result.split(',')[1]; // Remove data URL prefix
                resolve(base64String);
            };

            reader.onerror = (error) => {
                reject(error);
            };

            reader.readAsDataURL(file); // This converts the file into a base64 string
        });
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            encodeImageToBase64(file)
                .then((base64String) => {
                    const image = base64String;
                    setNewProfilePicture(`data:image/jpg;base64,${image}`); // Temporarily display the new image
                    setProfile({ ...profile, profile_picture: image }); // Save the file object for upload
                })
                .catch((error) => {
                    console.error('Error encoding image:', error);
                });
        }
    };

    // On submit, post updated user profile data to the backend API
    const handleSubmit = () => {
        axios.put("http://127.0.0.1:5000/api/profile/" + profile.profile_id, {
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
                            <img
                                src={newProfilePicture || `data:image/jpg;base64,${profile.profile_picture}`}
                                alt="Profile"
                                className="profile-image"
                            />
                            {fields.map((field) => (
                                <p key={field.name}>
                                    <strong>{field.label}:</strong> {field.value}
                                </p>
                            ))}
                        </div>
                        {/* Toggle edit mode button */}
                        <Button className="btn" onClick={() => setEdit(true)}>Edit</Button>
                    </>
                ) : (
                    /* If edit mode is on, display the data as text fields that can be editted and submitted */
                    <>
                        {/* Profile Picture Replace Button */}
                        <div className="imageUpload">
                            <img
                                src={newProfilePicture || `data:image/jpg;base64,${profile.profile_picture}`}
                                alt="Profile"
                                className="profile-image"
                            />
                            <input
                                type="file"
                                accept="image/*"
                                id="profile-picture"
                                style={{ display: "none" }}
                                onChange={handleImageChange}
                            />
                            <Button
                                className="btn"
                                component="label"
                                htmlFor="profile-picture"
                            >
                                Choose File
                            </Button>
                        </div>
                        {fields.map((field) => (
                            <TextField
                                key={field.name}
                                className={`input ${field.name === 'bio' ? 'bio' : 'shortField'}`}
                                style={{ display: "flex", ...field.style }}
                                label={field.label}
                                name={field.name}
                                type={field.type}
                                variant="outlined"
                                value={profile[field.name]}
                                onChange={(e) => setProfile({ ...profile, [e.target.name]: e.target.value })}
                                required
                                multiline={field.multiline}
                                rows={field.rows}
                                maxrows={field.maxrows}
                                fullWidth={field.fullWidth}
                            />
                        ))}
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
        profile_id: PropTypes.number,
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
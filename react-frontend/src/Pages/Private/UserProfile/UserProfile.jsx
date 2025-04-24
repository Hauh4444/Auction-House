// External Libraries
import { useEffect, useState } from "react";
import { Button, Card, CardContent, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { encodeImageToBase64 } from "@/utils/helpers"

// Stylesheets
import "./UserProfile.scss";

/**
 * UserProfile Component
 *
 * This component renders the profile page, which includes a header, a profile card,
 * and a right-side navigation panel. The main content is displayed in the center, and additional
 * navigation options are available on the right. Users can toggle between viewing their profile
 * and editing their details, including their profile picture.
 *
 * Features:
 * - Fetches and displays profile data.
 * - Allows users to edit their profile, including personal details and profile picture.
 * - Provides a button to toggle between view and edit modes.
 * - Submits updated profile data to the backend API.
 *
 * @returns { JSX.Element } The rendered UserProfile page component.
 */
const UserProfile = () => {
    const [edit, setEdit] = useState(false); // State to toggle between view and edit modes
    const [profile, setProfile] = useState({}) // State to hold profile data

    // Fields to be displayed in the profile
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

    // Fetch profile data from the backend API
    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/profile/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => setProfile(res.data.profile)) // Set the user state
            .catch(err => console.error(err)); // Log errors if any
    }, []); 

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            encodeImageToBase64(file)
                .then((base64String) => setProfile({ ...profile, profile_picture: base64String }))
                .catch(err => console.error(err)); // Log errors if any
        }
    };

    // On submit, post updated profile data to the backend API
    const handleSubmit = () => {
        // TODO All put and post requests need to be setup to send arguments like this
        axios.put(`${ import.meta.env.VITE_BACKEND_API_URL }/user/profile/${profile.profile_id}/`, profile,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensure cookies are sent if needed
            })
            .then(() => { setEdit(false) }) // Turn edit mode off if no errors
            .catch(err => console.error(err)); // Log errors if any
    }

    return (
        <div className="userProfilePage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                { /* Profile Card */ }
                <h1>Your Profile</h1>
                <Card className="userProfileCard">
                    <CardContent className="content">
                        {!edit ? (
                            /* If edit mode is off, display the data */
                            <>
                                <div className="profileInfo">
                                    <img
                                        src={ profile.profile_picture ? `data:image/jpg;base64,${ profile.profile_picture }` : "" }
                                        alt="Profile"
                                        className="profile-image"
                                    />
                                    {fields.map((field) => (
                                        <p key={ field.name }>
                                            <strong>{ field.label }:</strong> { field.value }
                                        </p>
                                    ))}
                                </div>
                                { /* Toggle edit mode button */ }
                                <Button className="btn" onClick={ () => setEdit(true) }>Edit</Button>
                            </>
                        ) : (
                            /* If edit mode is on, display the data as text fields that can be editted and submitted */
                            <>
                                { /* Profile Picture Replace Button */ }
                                <div className="imageUpload">
                                    <img
                                        src={ profile.profile_picture ? `data:image/jpg;base64,${ profile.profile_picture }` : "" }
                                        alt="Profile"
                                        className="profile-image"
                                    />
                                    <input
                                        type="file"
                                        accept="image/*"
                                        id="profile-picture"
                                        style={ { display: "none" } }
                                        onChange={ handleImageChange }
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
                                        key={ field.name }
                                        className={ `input ${ field.name === "bio" ? "bio" : "shortField"  }`}
                                        style={ { display: "flex", ...field.style } }
                                        label={ field.label }
                                        name={ field.name }
                                        type={ field.type }
                                        variant="outlined"
                                        value={ profile[field.name] }
                                        onChange={ (e) => setProfile({ ...profile, [e.target.name]: e.target.value  })}
                                        required
                                        multiline={ field.multiline }
                                        rows={ field.rows }
                                        maxrows={ field.maxrows }
                                        fullWidth={ field.fullWidth }
                                    />
                                ))}
                                { /* Submit button */ }
                                <Button className="btn" onClick={ () => handleSubmit(profile) }>Submit</Button>
                            </>
                        )}
                    </CardContent>
                </Card>
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
}

export default UserProfile;
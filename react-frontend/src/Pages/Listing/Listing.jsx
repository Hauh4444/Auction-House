// External Libraries
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
// Stylesheets
import "./Listing.scss";


const Listing = () => {
    const [listing, setListing] = useState({}); // State to store listing data
    const location = useLocation(); // Accessing the current location object from react-router-dom
    const queryParams = new URLSearchParams(location.search); // Parsing query parameters from the URL

    // useEffect hook to fetch listing data from the API when the component mounts
    useEffect(() => {
        // Sending GET request to fetch a specific listing based on the 'key' query parameter in the URL
        axios.get("http://127.0.0.1:5000/api/listings/" + queryParams.get("key"), {
            headers: {
                "Content-Type": "application/json", // Setting the request content type to JSON
            },
        })
            .then(res => {
                // If successful, set the listing data in the state
                setListing(res.data);
            })
            .catch(err => {
                // Log error in case of failure
                console.log(err);
            });
    }, []); // Empty dependency array means this effect will run only once when the component mounts

    return (
        <div className="listingPage">
            <div className="mainPage">
                <Header />
                <div className="listing">
                    <div className="listingInfo">
                        <div className="listingTitle">{listing.title}</div>
                        <div className="listingPrice">{listing.price}</div>
                        <Button className="addCartBtn">Add to Cart</Button>
                    </div>
                    <div className="listingImage">
                        {/* Checking if image data exists; if yes, displaying image, otherwise a fallback message */}
                        {listing.image_encoded ? (
                            <img src={"data:image/jpg;base64," + listing.image_encoded} alt={listing.title} />
                        ) : (
                            <div>No image available</div>
                        )}
                    </div>
                    <div className="listingDescription">
                        <div className="descriptionTitle">Description:</div>
                        {/* If the description is an array and has data, display it as a list */}
                        {Array.isArray(listing.description) && listing.description.length > 0 ? (
                            <ul className="descriptionList">
                                {listing.description.map((desc, i) => (
                                    <li key={i}>{desc}</li>
                                ))}
                            </ul>
                        ) : (
                            <div>No description available</div> // Fallback message if no description is available
                        )}
                    </div>
                </div>
            </div>
            <RightNavigation />
        </div>
    )
}

export default Listing;
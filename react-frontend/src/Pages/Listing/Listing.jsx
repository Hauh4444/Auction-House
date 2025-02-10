// External Libraries
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import ListingMain from "@/Components/ListingMain/ListingMain"
import ListingSpecifics from "@/Components/ListingSpecifics/ListingSpecifics"
import ListingReviews from "@/Components/ListingReviews/ListingReviews"
// Stylesheets
import "./Listing.scss";

const Listing = () => {
    const [listing, setListing] = useState({}); // State to store listing data
    const location = useLocation(); // Accessing the current location object from react-router-dom

    // useEffect hook to fetch listing data from the API when the component mounts
    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        // Sending GET request to fetch a specific listing based on the 'key' query parameter in the URL
        axios.get("http://127.0.0.1:5000/api/listings/" + filters.key, {
            headers: {
                "Content-Type": "application/json", // Setting the request content type to JSON
            },
        })
            .then(res => setListing(res.data))
            .catch(err => console.log(err));
    }, [location.search]); // Empty dependency array means this effect will run only once when the component mounts

    return (
        <div className="listingPage">
            <div className="mainPage">
                <Header />
                <div className="listing">
                    <ListingMain listing={listing} />
                    <div className="lesserInfo">
                        <ListingSpecifics listing={listing} />
                        <ListingReviews listing={listing} />
                    </div>
                </div>
            </div>
            <RightNavigation />
        </div>
    )
}

export default Listing;
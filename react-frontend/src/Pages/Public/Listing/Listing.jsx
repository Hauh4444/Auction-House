// External Libraries
import { useEffect, useState } from  "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import Main from "@/Components/Listing/Main/Main";
import Specifics from "@/Components/Listing/Specifics/Specifics";
import Reviews from "@/Components/Listing/Reviews/Reviews";

// Stylesheets
import "./Listing.scss";

/**
 * Listing Component
 *
 * This component fetches and displays a listing based on query parameters from the URL.
 * It utilizes React"s `useEffect` and `useState` hooks to manage the API request and state updates.
 *
 * Features:
 * - Retrieves listing data from the Flask server using Axios.
 * - Displays listing details using child components.
 * - Includes a navigation bar and header.
 *
 * @returns {JSX.Element} The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
 */
const Listing = () => {
    // State to store the listing data
    const [listing, setListing] = useState({});

    const location = useLocation(); // Hook to access the current location (URL)
    // Extract query parameters from the URL
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    /**
     * Fetches listing data based on the "key" parameter in the URL.
     * The effect runs every time `location.search` changes.
     */
    useEffect(() => {
        // API call to fetch the listing data
        axios.get("http://127.0.0.1:5000/api/listings/" + filters.key, {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => setListing(res.data.listing)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]); // Call on update of URL filters

    return (
        <div className="listingPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                <div className="listing">
                    {/* Main listing details */}
                    <Main listing={listing} />
                    <div className="lesserInfo">
                        {/* Additional listing information */}
                        <Specifics listing={listing} />
                        {/* Reviews section */}
                        <Reviews listing_id={listing.listing_id} />
                    </div>
                </div>
            </div>
            {/* Right-side navigation */}
            <RightNav />
        </div>
    );
}

export default Listing;

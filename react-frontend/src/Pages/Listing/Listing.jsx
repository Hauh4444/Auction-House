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
    const [listing, setListing] = useState({});
    const location = useLocation();

    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        axios.get("http://127.0.0.1:5000/api/listings/" + filters.key, {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => setListing(res.data))
            .catch(err => console.log(err));
    }, [location.search]);

    return (
        <div className="listingPage">
            <div className="mainPage">
                <Header />
                <div className="listing">
                    <ListingMain listing={listing} />
                    <div className="lesserInfo">
                        <ListingSpecifics listing={listing} />
                        <ListingReviews listing_id={listing.listing_id} />
                    </div>
                </div>
            </div>
            <RightNavigation />
        </div>
    )
}

export default Listing;
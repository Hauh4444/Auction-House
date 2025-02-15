// External Libraries
import { useEffect, useState } from  "react";
import { useLocation } from  "react-router-dom";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import Main from "@/Components/Listing/Main/Main"
import Specifics from "@/Components/Listing/Specifics/Specifics"
import Reviews from "@/Components/Listing/Reviews/Reviews"
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
                <Header/>
                <div className="listing">
                    <Main listing={listing}/>
                    <div className="lesserInfo">
                        <Specifics listing={listing}/>
                        <Reviews listing_id={listing.listing_id}/>
                    </div>
                </div>
            </div>
            <RightNav/>
        </div>
    )
}

export default Listing;
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
import SearchBar from "@//Components/SearchBar/SearchBar";
import LeftNavigation from "@//Components/LeftNavigation/LeftNavigation";
=======
import Header from "@/Components/Header/Header";
>>>>>>> 9d377c2 (update)
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
>>>>>>> 7ffa840 (WIP on main)
import "./Listing.scss";

const Listing = () => {
    const [listing, setListing] = useState({});
    const location = useLocation();

    useEffect(() => {
<<<<<<< HEAD
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        axios.get("http://127.0.0.1:5000/api/listings/" + filters.key, {
=======
        axios.get("http://127.0.0.1:5000/api/listings/" + queryParams.get("key"), {
>>>>>>> 7ffa840 (WIP on main)
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => setListing(res.data))
            .catch(err => console.log(err));
    }, [location.search]);

    return (
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 9d377c2 (update)
        <div className="listingPage">
            <div className="mainPage">
                <Header />
                <div className="listing">
<<<<<<< HEAD
                    <ListingMain listing={listing} />
                    <div className="lesserInfo">
                        <ListingSpecifics listing={listing} />
                        <ListingReviews listing_id={listing.listing_id} />
=======

        <div className="searchPage">
            <div style={{height: "100%", display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "70%"}}>
                    <SearchBar />
                    <div className="mainPage">
                        <div className="headNav">

=======
                    <div className="listingInfo">
                        <div className="listingTitle">
                            {listing.title}
>>>>>>> 9d377c2 (update)
                        </div>
                        <div className="listingPrice">
                            ${listing.price}
                        </div>
<<<<<<< HEAD
>>>>>>> 7ffa840 (WIP on main)
=======
                        <Button className="addCartBtn">
                            Add to Cart
                        </Button>
                    </div>
                    <div className="listingImage">
                        <img src={"data:image/jpg;base64," + listing.image} alt="" />
                    </div>
                    <div className="listingDescription">

>>>>>>> 9d377c2 (update)
                    </div>
                </div>
            </div>
<<<<<<< HEAD
<<<<<<< HEAD
            <RightNavigation />
=======
>>>>>>> 7ffa840 (WIP on main)
=======
            <RightNavigation />
>>>>>>> 9d377c2 (update)
        </div>
    )
}

export default Listing;
import Header from "@/Components/Header/Header";
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
import "./Listing.scss";

const Listing = () => {
    const [listing, setListing] = useState({});
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/listings/" + queryParams.get("key"), {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => {
                setListing(res.data.listing);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    return (
        <div className="listingPage">
            <div className="mainPage">
                <Header />
                <div className="listing">
                    <div className="listingInfo">
                        <div className="listingTitle">
                            {listing.title}
                        </div>
                        <div className="listingPrice">
                            ${listing.price}
                        </div>
                        <Button className="addCartBtn">
                            Add to Cart
                        </Button>
                    </div>
                    <div className="listingImage">
                        <img src={"data:image/jpg;base64," + listing.image} alt="" />
                    </div>
                    <div className="listingDescription">

                    </div>
                </div>
            </div>
            <RightNavigation />
        </div>
    )
}

export default Listing;
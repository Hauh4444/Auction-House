import { useState, useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { IoStar } from "react-icons/io5";
import { Button } from "@mui/material";
import axios from "axios";
import "./Listings.scss";
import { variables } from "@/assets/variables.modules.js"

const Listings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            q: queryParams.get("q"),
            c: queryParams.get("c"),
            sort: queryParams.get("sort"),
        })
            .then(res => {
                setListings(res.data.listings);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    function navigateToListing(listing) {
        navigate({
            pathname: "/listings",
            search: createSearchParams({
                key: listing.id
            }).toString(),
        });
    }

    return (
        <div className="listingsContainer">
            {listings.map((listing, index) => (
                <div className="listing" key={index}>
                    <div className="listingImage">
                        <img src={"data:image/jpg;base64," + listing.image} alt="" />
                    </div>
                    <div className="listingDescription">
                        <Button className="listingTitle" onClick={() => navigateToListing(listing)}>
                            {listing.title}
                        </Button>
                        <div className="listingReviews">
                            <IoStar style={{fontSize: "16px", color: variables.fontColor2}}/>
                            <IoStar style={{fontSize: "16px", color: variables.fontColor2}}/>
                            <IoStar style={{fontSize: "16px", color: variables.fontColor2}}/>
                            <IoStar style={{fontSize: "16px", color: variables.fontColor2}}/>
                            <IoStar style={{fontSize: "16px", color: variables.fontColor2}}/>
                            <span style={{
                                position: "relative",
                                top: "-3px",
                                fontSize: "12px",
                                color: variables.accentColor2,
                            }}>
                                &emsp;{listing.reviews}
                            </span>
                        </div>
                        <h1 className="listingPrice">
                            ${listing.price}
                        </h1>
                        <div className="bottomDetails">
                            <Button className="addCartBtn">
                                Add to Cart
                            </Button>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Listings;
import { useState, useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { LiaStarSolid , LiaStarHalfSolid } from "react-icons/lia";
import { Button } from "@mui/material";
import axios from "axios";
import "./Listings.scss";

const Listings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const filters = {};
        for (let [key, value] of queryParams.entries()) {
            filters[key] = value;
        }
        if (filters["p"]) {
            filters["start"] = ((filters["p"] - 1) * 50 + 1).toString();
            filters["end"] = (filters["p"] * 50).toString();
        }

        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                query: filters["q"],
                category: filters["c"],
                sort: filters["s"],
                start: filters["start"],
                end: filters["end"],
                type: filters["t"],
                other: filters["o"],
            }
        })
            .then(res => {
                setListings(res.data.listings);
            })
            .catch(err => {
                console.log(err);
            });
    }, [location.search]);

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
                    <div className="listingInfo">
                        <Button className="listingTitle" onClick={() => navigateToListing(listing)}>
                            {listing.title}
                        </Button>
                        <div className="listingReviews">
                            {Array.from({length: 5}, (_, i) =>
                                <LiaStarSolid className="blankStar" key={i} />
                            )}
                            {Array.from({ length: listing.stars }, (_, i) =>
                                <LiaStarSolid className="filledStar" key={i} />
                            )}
                            {listing.stars > Math.floor(listing.stars) &&
                                <LiaStarHalfSolid className="halfStar" />
                            }
                            <span className="reviews" style={{left: (-16 * Math.ceil(listing.stars) + "px"),}}>
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
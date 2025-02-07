// External Libraries
import { useState, useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { LiaStarSolid, LiaStarHalfSolid } from "react-icons/lia";
import { Button } from "@mui/material";
import axios from "axios";
// Stylesheets
import "./CategoryListings.scss";

const SearchListings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const filters = Object.fromEntries(queryParams.entries());

        filters.sort = filters.nav === "new" ? "created_at" : (filters.nav === "best" ? "purchases" : filters.sort);
        filters.order = filters.nav === "new" || filters.nav === "best" ? "desc" : filters.order;

        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                query: filters.query,
                category: filters.category,
                sort: filters.sort,
                order: filters.order,
                start: 1,
                end: 8,
                type: filters.type,
                other: filters.other,
            }
        })
            .then(res => setListings(res.data))
            .catch(err => console.log(err));
    }, [location.search]);

    function navigateToListing(id) {
        navigate({
            pathname: "/listings",
            search: createSearchParams({
                key: id
            }).toString(),
        });
    }

    return (
        <div className="categoryListings">
            {listings.map((listing, index) => (
                <div className={`listing ${index % 4 === 0 ? "first" : ""}`} key={index}>
                    <div className="listingImage">
                        <img src={"data:image/jpg;base64," + listing.image} alt="" />
                    </div>
                    <div className="listingInfo">
                        <div className="listingReviews">
                            {Array.from({ length: 5 }, (_, i) => (
                                <LiaStarSolid className="blankStar" key={i} />
                            ))}
                            {Array.from({ length: listing.average_review }, (_, i) => (
                                <LiaStarSolid className="filledStar" key={i} />
                            ))}
                            {listing.average_review > Math.floor(listing.average_review) && (
                                <LiaStarHalfSolid className="halfStar" />
                            )}
                            <span
                                className={"reviews"}
                                style={{ left: -16 * Math.ceil(listing.average_review) + "px" }}
                            >
                                &emsp;{listing.total_reviews}
                            </span>
                        </div>
                        <Button className="listingTitle" onClick={() => navigateToListing(listing.listing_id)}>
                            {listing.title_short}
                        </Button>
                        <h2 className="listingPrice">${listing.price}</h2>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default SearchListings;

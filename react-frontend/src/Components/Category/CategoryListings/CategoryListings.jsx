// External Libraries
import { useEffect, useState } from  "react";
import { createSearchParams, useLocation, useNavigate } from  "react-router-dom";
import { LiaStarHalfSolid, LiaStarSolid } from  "react-icons/lia";
import { Button } from  "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";
// Stylesheets
import "./CategoryListings.scss";
import "../Listings.scss"

const renderStars = (averageReview) => {
    const filledStars = Math.floor(averageReview);
    const halfStar = averageReview > filledStars;
    return (
        <span className="stars">
            {Array.from({length: 5}, (_, index) => (
                <LiaStarSolid className="blankStar" key={index}/>
            ))}
            {Array.from({length: filledStars}, (_, index) => (
                <LiaStarSolid className="filledStar" key={index}/>
            ))}
            {halfStar && <LiaStarHalfSolid className="halfStar"/>}
        </span>
    );
};

const CategoryListings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        if (filters.page) {
            filters.start = ((filters.page - 1) * 12).toString();
            filters.range = "12";
        }

        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: createSearchParams(filters),
        })
            .then(res => setListings(res.data))
            .catch(err => console.log(err));
    }, [location.search]);

    const navigateToListing = (id) => {
        navigate(`/listings?key=${id}`);
    }

    return (
        <>
            <h1 className="categoryListingsHead">View All</h1>
            <div className="categoryListings">
                {listings.map((listing, index) => (
                    <div className={`listing ${index % 4 === 0 ? "first" : ""}`} key={index}>
                        <div className="image">
                            <img src={"data:image/jpg;base64," + listing.image_encoded} alt=""/>
                        </div>
                        <div className="info">
                            <div className="review">
                                {renderStars(listing.average_review)}
                                <span className="totalReviews"
                                      style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                    &emsp;{listing.total_reviews}
                                </span>
                            </div>
                            <Button className="title" onClick={() => navigateToListing(listing.listing_id)}>
                                {listing.title_short}
                            </Button>
                            <h2 className="price">${listing.buy_now_price}</h2>
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
};

CategoryListings.propTypes = {
    bestSellers: PropTypes.shape({
        listing_id: PropTypes.number,
        title_short: PropTypes.string,
        buy_now_price: PropTypes.number,
        image_encoded: PropTypes.string,
        average_review: PropTypes.number,
        total_reviews: PropTypes.number,
    }),
};

export default CategoryListings;

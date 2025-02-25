// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { LiaStarHalfSolid, LiaStarSolid } from "react-icons/lia";
import { Button } from "@mui/material";
import PropTypes from "prop-types";
import axios from "axios";

// Stylesheets
import "./SearchListings.scss";

/**
 * Renders the star rating based on the average review score.
 * It will display filled, empty, or half stars accordingly.
 *
 * @param {number} averageReview - The average review score of the product.
 * @returns {JSX.Element} A span element with the appropriate number of stars.
 */
const renderStars = (averageReview) => {
    const filledStars = Math.floor(averageReview);
    const halfStar = averageReview > filledStars;
    return (
        <span className="stars">
            {/* Render empty stars */}
            {Array.from({length: 5}, (_, index) => (
                <LiaStarSolid className="blankStar" key={index} />
            ))}
            {/* Render filled stars */}
            {Array.from({length: filledStars}, (_, index) => (
                <LiaStarSolid className="filledStar" key={index} />
            ))}
            {/* Render half star if needed */}
            {halfStar && <LiaStarHalfSolid className="halfStar" />}
        </span>
    );
};

/**
 * SearchListings Component
 *
 * This component fetches and displays a list of product listings based on the
 * current search filters specified in the URL. It supports pagination, sorting
 * by various criteria such as creation date and purchase count, and provides
 * a visual representation of average reviews using star ratings. Users can click
 * on a listing to navigate to its detailed view or add it to their cart.
 *
 * Features:
 * - Fetches listings from a specified API based on URL parameters.
 * - Displays average reviews using a star rating system.
 * - Supports pagination and sorting based on various criteria.
 * - Navigates to a detailed listing view upon user interaction.
 *
 * @returns {JSX.Element} The rendered component containing a list of product
 *                        listings, each with an image, title, review stars,
 *                        price, and an "Add to Cart" button.
 */
const SearchListings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        if (filters.page) {
            filters.start = ((filters.page - 1) * 10).toString();
            filters.range = "10";
        }
        if (filters.nav === "new") {
            filters.sort = "created_at";
            filters.order = "desc";
        }
        if (filters.nav === "best-sellers") {
            filters.sort = "purchases";
            filters.order = "desc";
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
        navigate(`/listing?key=${id}`);
    }

    return (
        <div className="searchListings">
            {listings.map((listing, index) => (
                <div className="listing" key={index}>
                    <div className="image">
                        <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                    </div>
                    <div className="info">
                        <Button className="title" onClick={() => navigateToListing(listing.listing_id)}>
                            {listing.title}
                        </Button>
                        <div className="review">
                            {renderStars(listing.average_review)}
                            <span className="totalReviews"
                                  style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                &emsp;{listing.total_reviews}
                            </span>
                        </div>
                        <h2 className="price">
                            ${listing.buy_now_price}
                        </h2>
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

// Define the expected shape of the bestSellers prop
SearchListings.propTypes = {
    bestSellers: PropTypes.shape({
        listing_id: PropTypes.number,
        title_short: PropTypes.string,
        buy_now_price: PropTypes.number,
        image_encoded: PropTypes.string,
        average_review: PropTypes.number,
        total_reviews: PropTypes.number,
    }),
};

export default SearchListings;
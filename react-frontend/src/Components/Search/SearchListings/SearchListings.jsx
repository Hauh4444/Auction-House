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
    const filledStars = Math.floor(averageReview); // Calculate number of filled stars
    const halfStar = averageReview > filledStars; // Check if half star is needed
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
    const [listings, setListings] = useState([]); // State to hold product listings
    const navigate = useNavigate(); // Hook for navigation
    const location = useLocation(); // Hook to access the current location (URL)

    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract filters from URL

        // Adjust filters for pagination
        if (filters.page) {
            filters.start = ((filters.page - 1) * 10).toString();
            filters.range = "10";
        }
        // Apply sorting logic based on filter (new or best-sellers)
        if (filters.nav === "new") {
            filters.sort = "created_at";
            filters.order = "desc";
        }
        if (filters.nav === "best-sellers") {
            filters.sort = "purchases";
            filters.order = "desc";
        }

        // Fetch listings from the API with the specified filters
        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: createSearchParams(filters), // Convert filters to query parameters
        })
            .then(res => setListings(res.data.listings)) // Set the fetched listings into state
            .catch(err => console.log(err)); // Handle errors
    }, [location.search]); // Re-run the effect whenever search params change

    // Function to navigate to a detailed view of a listing
    const navigateToListing = (id) => {
        navigate(`/listing?key=${id}`);
    }

    return (
        <div className="searchListings">
            {listings.map((listing, index) => (
                <div className="listing" key={index}>
                    <div className="image">
                        {/* Display the product image */}
                        <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                    </div>
                    <div className="info">
                        {/* Button to navigate to the detailed listing view */}
                        <Button className="title" onClick={() => navigateToListing(listing.listing_id)}>
                            {listing.title}
                        </Button>
                        <div className="review">
                            {/* Render the star rating based on the average review */}
                            {renderStars(listing.average_review)}
                            {/* Display the total number of reviews */}
                            <span className="totalReviews"
                                  style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                &emsp;{listing.total_reviews}
                            </span>
                        </div>
                        <h2 className="price">
                            ${listing.buy_now_price} {/* Display the product price */}
                        </h2>
                        <div className="bottomDetails">
                            {/* Button to add the product to the cart */}
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

// Define the expected shape of the listings prop
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

// External Libraries
import { useEffect, useState } from  "react";
import { useLocation, useNavigate } from  "react-router-dom";
import { LiaStarHalfSolid, LiaStarSolid } from  "react-icons/lia";
import { Button } from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Stylesheets
import "./NewListings.scss";
import "../Listings.scss";

/**
 * Renders the star rating based on the average review score.
 * It will display filled, empty, or half stars accordingly.
 *
 * @param {number} averageReview - The average review score of the product.
 * @returns {JSX.Element} A span element with the appropriate number of stars.
 */
const renderStars = (averageReview) => {
    const filledStars = Math.floor(averageReview); // Number of filled stars
    const halfStar = averageReview > filledStars; // Check if there is a half star
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
 * NewListings component fetches and displays the newest product listings from an API.
 * Listings are retrieved based on the selected category and sorted by creation date.
 * Each listing includes an image, title, price, and review rating.
 *
 * Features:
 * - Fetches the latest listings from "http://127.0.0.1:5000/api/listings" when mounted or when filters change.
 * - Uses URL query parameters to filter listings by category.
 * - Displays listings with images, ratings, and a button to navigate to the listing's details page.
 *
 * @returns {JSX.Element} A section displaying the newest listings.
 */
const NewListings = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    // Extract query parameters from the URL
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    const [newListings, setNewListings] = useState([]); // State to hold new listings data

    // Effect hook to fetch listings from the API on component mount and URL filter update
    useEffect(() => {
        // Fetch new listings from the backend API
        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                category_id: filters.category_id, // Filter by category ID
                sort: "created_at", // Sort by creation date
                order: "desc", // Order by descending (newest first)
                start: 0, // Starting position
                range: 8, // Number of listings to fetch
            }
        })
            .then(res => setNewListings(res.data.listings)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]);// Call on update of URL filters

    // Navigate to a specific listing page when a listing is clicked
    const navigateToListing = (id) => {
        navigate(`/listing?key=${id}`);
    };

    return (
        <>
            <h1 className="categoryNewListingsHead">New</h1>
            <div className="categoryNewListings">
                {/* Map through the new listings and display them */}
                {newListings.map((listing, index) => (
                    <div className={`listing ${index === 0 ? "first" : ""}`} key={index}>
                        <div className="image">
                            <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                        </div>
                        <div className="info">
                            <div className="review">
                                {renderStars(listing.average_review)} {/* Render the star ratings */}
                                <span className="totalReviews"
                                      style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                    &emsp;{listing.total_reviews} {/* Display the total reviews */}
                                </span>
                            </div>
                            <Button className="title" onClick={() => navigateToListing(listing.listing_id)}>
                                {listing.title_short} {/* Display the listing title */}
                            </Button>
                            <h2 className="price">${listing.buy_now_price}</h2> {/* Display the price */}
                        </div>
                    </div>
                ))}
            </div>
        < />
    );
};

// Define the expected shape of the listing prop
NewListings.propTypes = {
    listing: PropTypes.shape({
        listing_id: PropTypes.number,
        title_short: PropTypes.string,
        buy_now_price: PropTypes.number,
        image_encoded: PropTypes.string,
        average_review: PropTypes.number,
        total_reviews: PropTypes.number,
    }),
};

export default NewListings;

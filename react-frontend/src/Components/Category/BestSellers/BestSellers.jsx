// External Libraries
import { useEffect, useState } from  "react";
import { useLocation, useNavigate } from  "react-router-dom";
import { LiaStarHalfSolid, LiaStarSolid } from  "react-icons/lia";
import { Button } from  "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Stylesheets
import "./BestSellers.scss"
import "../Listings.scss"

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
                <LiaStarSolid className="blankStar" key={index}/>
            ))}
            {/* Render filled stars */}
            {Array.from({length: filledStars}, (_, index) => (
                <LiaStarSolid className="filledStar" key={index}/>
            ))}
            {/* Render half star if needed */}
            {halfStar && <LiaStarHalfSolid className="halfStar"/>}
        </span>
    );
};

const BestSellers = () => {
    const navigate = useNavigate(); // Navigate function for routing
    const location = useLocation(); // Hook to access the current location (URL)
    // Extract query parameters from the URL
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    const [bestSellers, setBestSellers] = useState([]); // State to hold best sellers data

    // Effect hook to fetch listings from the API on component mount and URL filter update
    useEffect(() => {
        // Fetch best sellers from the backend API
        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                category_id: filters.category_id, // Apply category filter
                sort: "purchases", // Sort by number of purchases
                order: "desc", // Order in descending order
                start: 0, // Start from the first item
                range: 8, // Limit to 8 items
            }
        })
            .then(res => setBestSellers(res.data)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]); // Re-run effect if the location.search changes

    // Navigate to a specific listing page when a listing is clicked
    const navigateToListing = (id) => {
        navigate(`/listing?key=${id}`);
    };

    return (
        <>
            <h1 className="categoryBestSellersHead">Best Sellers</h1>
            <div className="categoryBestSellers">
                {/* Map through the best sellers and display them */}
                {bestSellers.map((listing, index) => (
                    <div className={`listing ${index === 0 ? "first" : ""}`} key={index}>
                        <div className="image">
                            <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt=""/>
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
        </>
    )
}

// Define the expected shape of the listing prop
BestSellers.propTypes = {
    listing: PropTypes.shape({
        listing_id: PropTypes.number,
        title_short: PropTypes.string,
        buy_now_price: PropTypes.number,
        image_encoded: PropTypes.string,
        average_review: PropTypes.number,
        total_reviews: PropTypes.number,
    }),
};

export default BestSellers;

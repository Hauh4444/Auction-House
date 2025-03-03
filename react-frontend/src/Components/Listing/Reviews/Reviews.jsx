// External Libraries
import { useEffect, useState } from "react";
import { LiaStarHalfSolid, LiaStarSolid } from "react-icons/lia";
import axios from "axios";
import PropTypes from "prop-types";

// Stylesheets
import "./Reviews.scss";

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
            {Array.from({ length: 5 }, (_, index) => (
                <LiaStarSolid className="blankStar" key={index} />
            ))}
            {/* Render filled stars */}
            {Array.from({ length: filledStars }, (_, index) => (
                <LiaStarSolid className="filledStar" key={index} />
            ))}
            {/* Render half star if needed */}
            {halfStar && <LiaStarHalfSolid className="halfStar" />}
        </span>
    );
};

/**
 * Reviews component fetches and displays user reviews for a given product listing.
 *
 * Features:
 * - Fetches reviews from the API based on the provided listing ID.
 * - Displays each review with the reviewer's username, review title, description, and date.
 * - Uses a star rating system to visually represent the rating score.
 * - Limits the display to the top three highest-rated reviews.
 *
 * @param {Object} props - Component props.
 * @param {number} props.listing_id - The unique ID of the listing for which reviews are fetched.
 *
 * @returns {JSX.Element} A section displaying user reviews.
 */
const Reviews = ({ listing_id }) => {
    const [reviews, setReviews] = useState([]);

    // Effect hook to fetch reviews from the API on component mount and URL filter update
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/reviews", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                listing_id: listing_id, // Apply listing_id parameter
                sort: "stars", // Sort by number of stars
                order: "desc", // Order in descending order
                start: 0, // Start from the first item
                range: 3, // Limit to 3 items
            },
        })
            .then((res) => setReviews(res.data.reviews)) // Update state with fetched data
            .catch((err) => console.log(err)); // Log errors if any
    }, [listing_id]);

    return (
        <div className="reviewSection">
            {reviews &&
                reviews.map((review, index) => (
                    <div className="review" key={index}>
                        <div className="left">
                            {renderStars(review.stars)}
                            <p>- by {review.username}</p>
                            <p className="date">{review.created_at}</p>
                        </div>
                        <div className="right">
                            <h3>{review.title}</h3>
                            <p>{review.description}</p>
                        </div>
                    </div>
                ))}
        </div>
    );
};

// Define the expected shape of the listing_id and reviews props
Reviews.propTypes = {
    listing_id: PropTypes.number,
};

export default Reviews;

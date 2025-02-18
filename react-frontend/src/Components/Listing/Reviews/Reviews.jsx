// External Libraries
import { useEffect, useState } from  "react";
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
            {Array.from({length: 5}, (_, index) => (
                <LiaStarSolid className="blankStar" key={index} />
            ))}
            {Array.from({length: filledStars}, (_, index) => (
                <LiaStarSolid className="filledStar" key={index} />
            ))}
            {halfStar && <LiaStarHalfSolid className="halfStar" />}
        </span>
    );
};

const Reviews = ({listing_id}) => {
    const [reviews, setReviews] = useState([]);

    // Effect hook to fetch reviews from the API on component mount and URL filter update
    useEffect(() => {
        // Fetch best sellers from the backend API
        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                listing_id: listing_id, // Apply listing_id parameter
                sort: "stars", // Sort by number of stars
                order: "desc", // Order in descending order
                start: 0, // Start from the first item
                range: 3, // Limit to 3 items
            }
        })
            .then(res => setReviews(res.data)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, []); // Empty dependency array to ensure it runs only once when the component is mounted

    return (
        <div className="reviewSection">
            {reviews && (
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
                ))
            )}
        </div>
    )
}

// Define the expected shape of the listing_id and reviews props
Reviews.propTypes = {
    listing_id: PropTypes.number,
    reviews: PropTypes.shape({
        username: PropTypes.string,
        title: PropTypes.string,
        description: PropTypes.string,
        stars: PropTypes.number,
        created_at: PropTypes.string,
    }),
};

export default Reviews;
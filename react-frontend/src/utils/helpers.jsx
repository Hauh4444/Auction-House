// External Libraries
import { LiaStarHalfSolid, LiaStarSolid } from "react-icons/lia";
import axios from "axios";

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
                <LiaStarSolid className="blankStar" data-testid="blankStar" key={index} />
            ))}
            {/* Render filled stars */}
            {Array.from({length: filledStars}, (_, index) => (
                <LiaStarSolid className="filledStar" data-testid="filledStar" key={index} />
            ))}
            {/* Render half star if needed */}
            {halfStar && <LiaStarHalfSolid className="halfStar" data-testid="halfStar" />}
        </span>
    );
};

const encodeImageToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onloadend = () => {
            // The result is the base64 encoded string
            const base64String = reader.result.split(",")[1]; // Remove data URL prefix
            resolve(base64String);
        };

        reader.onerror = (error) => {
            reject(error);
        };

        reader.readAsDataURL(file); // This converts the file into a base64 string
    });
};

// Navigate to a specific listing page when a listing is clicked
const navigateToListing = (id, navigate) => {
    navigate(`/listing?key=${id}`);
};

const addToList = (list_id, listing_id) => {
    axios.post(`${import.meta.env.BACKEND_URL}/user/lists/${list_id}/`,
        {
            listing_id: listing_id,
        },
        {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensure cookies are sent
        })
        .catch(err => console.log(err)); // Log errors if any
}

const updateList = (list_id, list_items) => {
    axios.put(`${import.meta.env.BACKEND_URL}/user/lists/${list_id}/`,
        {
            list_items: list_items,
        },
        {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensure cookies are sent
        })
        .catch(err => console.log(err)); // Log errors if any
}

export { renderStars, encodeImageToBase64, navigateToListing, addToList, updateList };
// External Libraries
import { LiaStarHalfSolid, LiaStarSolid } from "react-icons/lia";
import PropTypes from "prop-types";
// Stylesheets
import "./ListingReviews.scss";

const renderStars = (averageReview) => {
    const filledStars = Math.floor(averageReview);
    const halfStar = averageReview > filledStars;
    return (
        <span className="stars">
            {Array.from({ length: 5 }, (_, i) => (
                <LiaStarSolid className="blankStar" key={i} />
            ))}
            {Array.from({ length: filledStars }, (_, i) => (
                <LiaStarSolid className="filledStar" key={i} />
            ))}
            {halfStar && <LiaStarHalfSolid className="halfStar" />}
        </span>
    );
};

const ListingReviews = ({listing_id}) => {
    const reviews = [
        {
            "review_id": 1,
            "listing_id": 1,
            "user_id": 1,
            "title": "idk",
            "description": "It's good idk",
            "created_at": "Feb 10, 2025",
            "stars": 5,
        },
        {
            "review_id": 2,
            "listing_id": 1,
            "user_id": 1,
            "title": "Absolutely amazing",
            "description": "This is probably the best item I bought for the price it’s really amazing everything works perfectly and for the good condition it just has a little mark at the bottom that’s it. Incredible no scratches or anything on the main screen. Just watch band is small but can be easily replaced :) happy buying!",
            "created_at": "Feb 10, 2025",
            "stars": 5,
        },
        {
            "review_id": 3,
            "listing_id": 1,
            "user_id": 1,
            "title": "Value and quality apple watch",
            "description": "Great value, my watch was in excellent condition. No scratches. Charges well, I like the size of the watch- big but not so much that it overpowers my wrist. Love the features of ekg, cell, touch screen and the color.",
            "created_at": "Feb 10, 2025",
            "stars": 5,
        }
    ]

    const user = {
        "username": "mk4ds"
    }

    return (
        <div className="reviewSection">
            {reviews ? (
                reviews.map((review, index) => (
                    <div className="review" key={index}>
                        <div className="left">
                            {renderStars(review.stars)}
                            <p>- by {user.username}</p>
                            <p className="date">{review.created_at}</p>
                        </div>
                        <div className="right">
                            <h3>{review.title}</h3>
                            <p>{review.description}</p>
                        </div>
                    </div>
                ))
            ) : (
                <></>
            )}
        </div>
    )
}

ListingReviews.propTypes = {
    listing_id: PropTypes.number
};

export default ListingReviews;
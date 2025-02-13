// External Libraries
import {useEffect, useState} from "react";
import {createSearchParams, useLocation, useNavigate} from "react-router-dom";
import {LiaStarHalfSolid, LiaStarSolid} from "react-icons/lia";
import {Button} from "@mui/material";
import axios from "axios";
// Stylesheets
import "./CategoryListings.scss";

const renderStars = (averageReview) => {
    const filledStars = Math.floor(averageReview);
    const halfStar = averageReview > filledStars;
    return (
        <span className="stars">
            {Array.from({length: 5}, (_, i) => (
                <LiaStarSolid className="blankStar" key={i}/>
            ))}
            {Array.from({length: filledStars}, (_, i) => (
                <LiaStarSolid className="filledStar" key={i}/>
            ))}
            {halfStar && <LiaStarHalfSolid className="halfStar"/>}
        </span>
    );
};

const SearchListings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    if (filters.page) filters.start = ((filters.page - 1) * 12).toString(), filters.range = "12";

    useEffect(() => {
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
                            <div className="reviews">
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

export default SearchListings;

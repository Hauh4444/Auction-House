// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { LiaStarHalfSolid, LiaStarSolid } from "react-icons/lia";
import {Button} from "@mui/material";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import CategoryListings from "@/Components/CategoryListings/CategoryListings";
// Stylesheets
import "./Category.scss";
import {MdArrowBackIosNew, MdArrowForwardIos} from "react-icons/md";


const Category = () => {
    const [category, setCategory] = useState({}); // State to store category data
    const location = useLocation(); // Accessing the current location object from react-router-dom to read URL parameters
    const [bestSellers, setBestSellers] = useState([]);
    const [newListings, setNewListings] = useState([]);
    const navigate = useNavigate();

    // useEffect hook to fetch category data from the API when the component mounts or the URL changes
    useEffect(() => {
        // Parsing the URL query parameters
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        // Making a GET request to the backend to fetch category data based on the 'c' parameter from the URL
        axios.get("http://127.0.0.1:5000/api/categories/" + filters.category, {
            headers: {
                "Content-Type": "application/json", // Setting the request content type to JSON
            },
        })
            .then(res => {
                // If the request is successful, set the category data in the state
                setCategory(res.data);
            })
            .catch(err => {
                // Log any errors if the request fails
                console.log(err);
            });

        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                category: filters.category,
                sort: "purchases",
                order: "desc",
                start: 1,
                end: 8,
            }
        })
            .then(res => setBestSellers(res.data))
            .catch(err => console.log(err));

        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                category: filters.category,
                sort: "created_at",
                order: "desc",
                start: 1,
                end: 8,
            }
        })
            .then(res => setNewListings(res.data))
            .catch(err => console.log(err));
    }, [location.search]); // The effect will re-run whenever the 'location.search' (URL search query) changes

    function navigateToListing(id) {
        navigate({
            pathname: "/listings",
            search: createSearchParams({
                key: id
            }).toString(),
        });
    }

    return (
        <div className="categoryPage">
            <div className="mainPage">
                <Header />
                <div className="categoryHead">
                    <div className="categoryInfo">
                        <h1>{category.name}</h1>
                        <p>{category.description}</p>
                    </div>
                    <div className="categoryImg">
                        {/* If the category has an image, display it; otherwise, show a fallback message */}
                        {category.image_encoded ? (
                            <img
                                src={"data:image/jpg;base64," + category.image_encoded}
                                alt={category.title}
                            />
                        ) : (
                            <div>No image available</div> // Fallback text if there is no image
                        )}
                    </div>
                </div>
                <h1 className="categoryBestSellersHead">Best Sellers</h1>
                <div className="categoryBestSellers">
                    {bestSellers.map((listing, index) => (
                        <div className={`listing ${index === 0 ? "first" : ""}`} key={index}>
                            <div className="listingImage">
                                <img src={"data:image/jpg;base64," + listing.image_encoded} alt="" />
                            </div>
                            <div className="listingInfo">
                                <div className="listingReviews">
                                    {Array.from({ length: 5 }, (_, i) => (
                                        <LiaStarSolid className="blankStar" key={i} />
                                    ))}
                                    {Array.from({ length: listing.average_review }, (_, i) => (
                                        <LiaStarSolid className="filledStar" key={i} />
                                    ))}
                                    {listing.average_review > Math.floor(listing.average_review) && (
                                        <LiaStarHalfSolid className="halfStar" />
                                    )}
                                    <span
                                        className={"reviews"}
                                        style={{ left: -16 * Math.ceil(listing.average_review) + "px" }}
                                    >
                                &emsp;{listing.total_reviews}
                            </span>
                                </div>
                                <Button className="listingTitle" onClick={() => navigateToListing(listing.listing_id)}>
                                    {listing.title_short}
                                </Button>
                                <h2 className="listingPrice">${listing.buy_now_price}</h2>
                            </div>
                        </div>
                    ))}
                </div>
                <h1 className="categoryNewListingsHead">New</h1>
                <div className="categoryNewListings">
                    {newListings.map((listing, index) => (
                        <div className={`listing ${index === 0 ? "first" : ""}`} key={index}>
                            <div className="listingImage">
                                <img src={"data:image/jpg;base64," + listing.image_encoded} alt="" />
                            </div>
                            <div className="listingInfo">
                                <div className="listingReviews">
                                    {Array.from({ length: 5 }, (_, i) => (
                                        <LiaStarSolid className="blankStar" key={i} />
                                    ))}
                                    {Array.from({ length: listing.average_review }, (_, i) => (
                                        <LiaStarSolid className="filledStar" key={i} />
                                    ))}
                                    {listing.average_review > Math.floor(listing.average_review) && (
                                        <LiaStarHalfSolid className="halfStar" />
                                    )}
                                    <span
                                        className={"reviews"}
                                        style={{ left: -16 * Math.ceil(listing.average_review) + "px" }}
                                    >
                                &emsp;{listing.total_reviews}
                            </span>
                                </div>
                                <Button className="listingTitle" onClick={() => navigateToListing(listing.listing_id)}>
                                    {listing.title_short}
                                </Button>
                                <h2 className="listingPrice">${listing.buy_now_price}</h2>
                            </div>
                        </div>
                    ))}
                </div>
                <CategoryListings />
            </div>
            <RightNavigation />
        </div>
    )
}

export default Category;
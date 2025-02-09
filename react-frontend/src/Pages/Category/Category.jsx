// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { LiaStarHalfSolid, LiaStarSolid } from "react-icons/lia";
import { Button } from "@mui/material";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import CategoryListings from "@/Components/CategoryListings/CategoryListings";
// Stylesheets
import "./Category.scss";

// Helper function to render stars based on average review
const renderStars = (averageReview) => {
    const filledStars = Math.floor(averageReview); // Determine how many full stars should be rendered
    const halfStar = averageReview > filledStars; // Determine if there is a half star
    return (
        <>
            {Array.from({ length: 5 }, (_, i) => (
                <LiaStarSolid className="blankStar" key={i} />
            ))}
            {Array.from({ length: filledStars }, (_, i) => (
                <LiaStarSolid className="filledStar" key={i} />
            ))}
            {halfStar && <LiaStarHalfSolid className="halfStar" />}
        </>
    );
};

const Category = () => {
    // State variables to hold category data, best sellers, new listings, loading state, and error state
    const [category, setCategory] = useState({});
    const [bestSellers, setBestSellers] = useState([]);
    const [newListings, setNewListings] = useState([]);

    const navigate = useNavigate(); // To navigate to other pages programmatically
    const location = useLocation(); // To get the current URL and query parameters
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Get query parameters from the URL

    // Fetch data on component mount or when URL changes
    useEffect(() => {

        // Async function to fetch category, best sellers, and new listings data
        const fetchData = async () => {
            try {
                // Fetch category data based on the 'category' filter from URL
                const categoryResponse = await axios.get(`http://127.0.0.1:5000/api/categories/${filters.category_id}`);
                setCategory(categoryResponse.data); // Update the category state with the response data

                // Fetch best-selling listings data
                const bestSellersResponse = await axios.get("http://127.0.0.1:5000/api/listings", {
                    params: {
                        category_id: filters.category_id,
                        start: 0,
                        range: 8,
                    },
                });
                setBestSellers(bestSellersResponse.data); // Update best sellers state with the response data

                // Fetch new listings data
                const newListingsResponse = await axios.get("http://127.0.0.1:5000/api/listings", {
                    params: {
                        category_id: filters.category_id,
                        start: 0,
                        range: 8,
                    },
                });
                setNewListings(newListingsResponse.data); // Update new listings state with the response data
            } catch (err) {
                console.log(err); // Log the error to the console
            }
        };
        fetchData(); // Call the async function to fetch data
    }, [location.search]); // The effect depends on the 'location.search' value, so it will run whenever the URL changes

    // Function to navigate to a specific listing page
    const navigateToListing = (id) => {
        navigate(`/listings?key=${id}`);
    };

    // Function to handle pagination
    function pagination(n) {
        // Increment or decrement the page number (p) in filters
        filters.page = parseInt(filters.page) + n;
        // Update the URL with the new filters (this causes a re-render)
        navigate({
            pathname: "/category",
            search: createSearchParams(filters).toString(), // Convert filters object to query string
        });
        let obj = document.querySelector(".categoryListingsHead");
        let objTop = 0;
        if (obj.offsetParent) {
            do {
                objTop += obj.offsetTop;
            } while ((obj = obj.offsetParent));
        }
        window.scrollTo(0, objTop - 50);
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
                        {category.image_encoded ? (
                            <img src={`data:image/jpg;base64,${category.image_encoded}`} alt={category.title} />
                        ) : (
                            <div>No image available</div>
                        )}
                    </div>
                </div>
                <h1 className="categoryBestSellersHead">Best Sellers</h1>
                <div className="categoryBestSellers">
                    {bestSellers.map((listing, index) => (
                        <div className={`listing ${index === 0 ? "first" : ""}`} key={listing.listing_id}>
                            <div className="listingImage">
                                <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                            </div>
                            <div className="listingInfo">
                                <div className="listingReviews">
                                    {renderStars(listing.average_review)}
                                    <span className="reviews" style={{ left: -16 * Math.ceil(listing.average_review) + "px" }}>
                                        &emsp;{listing.total_reviews}
                                    </span>
                                </div>
                                <Button className="listingTitle" onClick={() => navigateToListing(listing.listing_id)}>
                                    {listing.title_short}
                                </Button>
                                <h2 className="listingPrice">${listing.current_price}</h2>
                            </div>
                        </div>
                    ))}
                </div>
                <h1 className="categoryNewListingsHead">New</h1>
                <div className="categoryNewListings">
                    {newListings.map((listing, index) => (
                        <div className={`listing ${index === 0 ? "first" : ""}`} key={listing.listing_id}>
                            <div className="listingImage">
                                <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                            </div>
                            <div className="listingInfo">
                                <div className="listingReviews">
                                    {renderStars(listing.average_review)}
                                    <span className="reviews" style={{ left: -16 * Math.ceil(listing.average_review) + "px" }}>
                                        &emsp;{listing.total_reviews}
                                    </span>
                                </div>
                                <Button className="listingTitle" onClick={() => navigateToListing(listing.listing_id)}>
                                    {listing.title_short}
                                </Button>
                                <h2 className="listingPrice">${listing.current_price}</h2>
                            </div>
                        </div>
                    ))}
                </div>
                <CategoryListings />
                <div className="pagination">
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon" />&ensp;Previous</Button>
                    <Button style={{ marginLeft: "25px" }} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos className="icon" /></Button>
                </div>
            </div>
            <RightNavigation />
        </div>
    );
};

export default Category;
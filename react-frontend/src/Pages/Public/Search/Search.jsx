// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { Button } from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Internal Modules
import Header from "@/Components/Header/Header";
import SearchNav from "@/Components/Navigation/SearchNav/SearchNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { renderStars, navigateToListing, addToList } from "@/utils/helpers";
import { useCart } from "@/ContextAPI/CartContext";

// Stylesheets
import "./Search.scss"

/**
 * Search Component
 *
 * This component handles search functionality and displays search results.
 * It includes pagination support for viewing multiple pages of results.
 *
 * Features:
 * - Retrieves query parameters from the URL.
 * - Displays search results with filters.
 * - Provides pagination buttons when "view-all" mode is enabled.
 *
 * @returns {JSX.Element} The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
 */
const Search = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL

    const { addToCart } = useCart(); // Access authentication functions from the AuthProvider context

    const [listings, setListings] = useState([]); // State to hold product listings
    const [paginationButtons, setPaginationButtons] = useState(null); // State to store the pagination buttons

    useEffect(() => {
        // Adjust filters for pagination
        if (filters.page) {
            filters.start = ((filters.page - 1) * 10).toString();
            filters.range = "10";
        }
        // Apply sorting logic based on filter (new or best-sellers)
        if (filters.nav === "new") {
            filters.sort = "created_at";
            filters.order = "desc";
            setPaginationButtons(null);
        }
        if (filters.nav === "best-sellers") {
            filters.sort = "purchases";
            filters.order = "desc";
            setPaginationButtons(null);
        }
        // Display pagination buttons if "view-all" navigation is selected
        if (filters.nav === "view-all") {
            setPaginationButtons(
                // Pagination buttons
                <div className="pagination">
                    <Button
                        className="previousPagination"
                        style={filters.page === "1" ? {opacity: 0.5, cursor: "default"} : {opacity: 1, cursor: "pointer"}}
                        disabled={filters.page === "1"}
                        onClick={() => pagination(-1)}
                    >
                        <MdArrowBackIosNew className="icon" />&ensp;Previous
                    </Button>
                    <Button
                        style={{marginLeft: "25px"}}
                        onClick={() => pagination(1)}
                    >
                        Next&ensp;<MdArrowForwardIos className="icon" />
                    </Button>
                </div>
            );
        }

        // Fetch listings from the API with the specified filters
        axios.get("http://127.0.0.1:5000/api/listings/", {
            headers: {
                "Content-Type": "application/json",
            },
            params: createSearchParams(filters), // Convert filters to query parameters
        })
            .then((res) => setListings(res.data.listings)) // Set the fetched listings into state
            .catch(() => setListings([])); // Log errors if any
    }, [location.search]);

    /**
     * Handles pagination for search results.
     * Adjusts the `page` parameter in the URL and reloads results.
     *
     * @param {number} n - Increment or decrement for pagination.
     */
    function pagination(n) {
        // Update URL filter
        filters.page = (parseInt(filters.page) + n).toString();
        // Navigate with new filters
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });

        // Scroll to top of page
        setTimeout(() => {
            window.scrollTo(0, 0);
        }, 100);
    }

    return (
        <div className="searchPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                {/* Search Navigation */}
                <SearchNav />
                {/* Search Listings */}
                <div className="searchListings">
                    {listings.map((listing, index) => (
                        <div
                            className={`listing ${index === listings.length - 1 && filters.nav !== "view-all" ? "last" : ""}`}
                            key={index}
                        >
                            <div className="image">
                                {/* Display the product image */}
                                <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                            </div>
                            <div className="info">
                                {/* Button to navigate to the detailed listing view */}
                                <Button className="title" onClick={() => navigateToListing(listing.listing_id, navigate)}>
                                    {listing.title}
                                </Button>
                                <div className="review">
                                    {/* Render the star rating based on the average review */}
                                    {renderStars(listing.average_review)}
                                    {/* Display the total number of reviews */}
                                    <span className="totalReviews" style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                        &emsp;{listing.total_reviews}
                                    </span>
                                </div>
                                <h2 className="price">
                                    ${listing.buy_now_price} {/* Display the product price */}
                                </h2>
                            </div>
                            <div className="btns">
                                <Button className="addToListBtn" onClick={() => addToList(1, listing.listing_id)}>Add To List</Button>
                                {/* Button to add the product to the cart */}
                                <Button className="addCartBtn" onClick={() => addToCart(listing)}>Add to Cart</Button>
                            </div>
                        </div>
                    ))}
                    {/* Pagination Controls */}
                    {paginationButtons}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

// Define the expected shape of the listings prop
Search.propTypes = {
    listing: PropTypes.shape({
        listing_id: PropTypes.number,
        title_short: PropTypes.string,
        buy_now_price: PropTypes.number,
        image_encoded: PropTypes.string,
        average_review: PropTypes.number,
        total_reviews: PropTypes.number,
    }),
};

export default Search;

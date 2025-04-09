// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { Button } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { renderStars, navigateToListing } from "@/utils/helpers";

// Stylesheets
import "./Category.scss";

/**
 * Category Component
 *
 * This component fetches and displays details for a specific category, including its name,
 * description, and image. It also provides functionality for pagination of category listings,
 * allowing users to navigate through different pages of listings.
 *
 * Features:
 * - Fetches category data from a backend API based on the "category_id" query parameter.
 * - Displays the category"s bestsellers, new listings, and specific category listings.
 * - Implements pagination using React Router, allowing users to navigate between pages of listings.
 *
 * @returns { JSX.Element } The rendered category page containing category information and listings.
 */
const Category = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters

    const [category, setCategory] = useState({}); // State to store the category data
    const [bestSellers, setBestSellers] = useState([]); // State to hold bestsellers data
    const [newListings, setNewListings] = useState([]); // State to hold new listings data
    const [listings, setListings] = useState([]); // State to hold listings data
    const sections = [
        {
            title: "Best Sellers",
            identifier: "BestSellers",
            listings: bestSellers,
        },
        {
            title: "New",
            identifier: "NewListings",
            listings: newListings,
        },
        {
            title: "View All",
            identifier: "Listings",
            listings: listings,
        },
    ]

    useEffect(() => {
        // API call to access the category data
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/categories/${ filters.category_id }/`, {
            headers: { "Content-Type": "application/json" },
        })
            .then((res) => setCategory(res.data.category)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]);

    useEffect(() => {
        // Fetch bestsellers from the backend API
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/`, {
            headers: { "Content-Type": "application/json" },
            params: {
                category_id: filters.category_id, // Apply category filter
                sort: "purchases", // Sort by number of purchases
                order: "desc", // Order in descending order
                start: 0, // Start from the first item
                range: 8, // Limit to 8 items
            }
        })
            .then((res) => setBestSellers(res.data.listings)) // Update state with fetched data
            .catch(() => setBestSellers([]));
    }, [location.search])

    useEffect(() => {
        // Fetch new listings from the backend API
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/`, {
            headers: { "Content-Type": "application/json" },
            params: {
                category_id: filters.category_id, // Filter by category ID
                sort: "created_at", // Sort by creation date
                order: "desc", // Order by descending (newest first)
                start: 0, // Starting position
                range: 8, // Number of listings to fetch
            }
        })
            .then((res) => setNewListings(res.data.listings)) // Update state with fetched data
            .catch(() => setNewListings([]));
    }, [location.search]);

    useEffect(() => {
        // Handle pagination by adjusting filters
        if (filters.page) {
            filters.start = ((filters.page - 1) * 12).toString(); // Start position for pagination
            filters.range = "12"; // Set the range (number of items per page)
        }

        // Fetch listings from the backend API
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/`, {
            headers: { "Content-Type": "application/json" },
            params: {
                category_id: filters.category_id, // Filter by category ID
                start: filters.start, // Starting position
                range: filters.range, // Number of listings to fetch
            }
        })
            .then((res) => setListings(res.data.listings)) // Update state with fetched data
            .catch(() => setListings([]));
    }, [location.search]); // Call on update of URL filters

    /**
     * Handles pagination for category listings.
     * Adjusts the `page` parameter in the URL and scrolls to the category listings.
     *
     * @param { number } n - Increment or decrement for pagination.
     */
    function pagination(n) {
        // Update URL filter
        filters.page = (parseInt(filters.page) + n).toString();
        // Navigate with new filters
        navigate({
            pathname: "/category",
            search: createSearchParams(filters).toString(),
        });

        // Calculate scroll position of top of pagination section and scroll
        setTimeout(() => {
            let obj = document.querySelector(".categoryListingsHead");
            if (obj) {
                let objTop = obj.getBoundingClientRect().top + window.scrollY;
                window.scrollTo({ top: objTop - 50, behavior: "smooth" });
            }
        }, 100);
    }

    return (
        <div className="categoryPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />
                <div className="head">
                    { /* Category Description */ }
                    <div className="info">
                        <h1 data-testid="categoryName">{ category.name }</h1>
                        <p data-testid="categoryDescription">{ category.description }</p>
                    </div>
                    { /* Category Image */ }
                    <div className="image">
                        {category.image_encoded ? (
                            <img
                                data-testid="categoryImage"
                                src={ `data:image/jpg;base64,${ category.image_encoded  }`}
                                alt={ category.name }
                            />
                        ) : (
                            <div>No image available</div>
                        )}
                    </div>
                </div>
                <div className="content">
                    { /* Category Sections */ }
                    {sections.map((section, index) => (
                        <div key={ index }>
                            <h1 className={ `categoryHead` }>{ section.title }</h1>
                            <div className={ `category${ section.identifier  }`}>
                                { /* Map through the bestsellers and display them */ }
                                {section.listings.map((listing, index) => (
                                    /* TODO FIX THIS STUPID HACKY BULLSHIT */
                                    <div className={`listing ${section.identifier !== "Listings" && index === 0 ? "first" :
                                        (section.identifier === "Listings" && index % 4 === 0 ? "first" : "")}`} key={ index }>
                                        <div className="image">
                                            <img src={ `data:image/jpg;base64,${ listing.image_encoded  }`} alt="" />
                                        </div>
                                        <div className="info">
                                            <div className="review">
                                                { renderStars(listing.average_review) } { /* Render the star ratings */ }
                                                <span className="totalReviews"
                                                      style={ { left: -16 * Math.ceil(listing.average_review) + "px" } }>
                                                &emsp;{ listing.total_reviews } { /* Display the total reviews */ }
                                            </span>
                                            </div>
                                            <Button
                                                className="title"
                                                onClick={ () => navigateToListing(listing.listing_id, navigate) }
                                            >
                                                { listing.title_short } { /* Display the listing title */ }
                                            </Button>
                                            <h2 className="price">${ listing.buy_now_price }</h2> { /* Display the price */ }
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}

                    { /* Pagination Controls */ }
                    <div className="pagination">
                        <Button
                            className="previousPagination"
                            style={ filters.page === "1" ? { opacity: 0.5, cursor: "default"  } : { opacity: 1, cursor: "pointer" } }
                            disabled={ filters.page === "1" }
                            onClick={ () => pagination(-1) }
                        >
                            <MdArrowBackIosNew className="icon" />&ensp;Previous
                        </Button>
                        <Button
                            style={ { marginLeft: "25px" } }
                            onClick={ () => pagination(1) }
                        >
                            Next&ensp;<MdArrowForwardIos className="icon" />
                        </Button>
                    </div>
                </div>
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
};

export default Category;

// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { Button } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import CategoryListings from "@/Components/Category/CategoryListings/CategoryListings";
import BestSellers from "@/Components/Category/BestSellers/BestSellers";
import NewListings from "@/Components/Category/NewListings/NewListings";

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
 * - Displays the category"s best sellers, new listings, and specific category listings.
 * - Implements pagination using React Router, allowing users to navigate between pages of listings.
 *
 * @returns {JSX.Element} The rendered category page containing category information and listings.
 */
const Category = () => {
    // State to store the category data
    const [category, setCategory] = useState({});

    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    // Extract query parameters
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    /**
     * Fetches category data based on the "category_id" parameter.
     * The effect runs every time `location.search` changes.
     */
    useEffect(() => {
        // API call to access the category data
        axios.get(`http://127.0.0.1:5000/api/categories/${filters.category_id}`, {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => setCategory(res.data.category)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]); // Call on update of URL filters

    /**
     * Handles pagination for category listings.
     * Adjusts the `page` parameter in the URL and scrolls to the category listings.
     *
     * @param {number} n - Increment or decrement for pagination.
     */
    function pagination(n) {
        // Update URL filter
        filters.page = (parseInt(filters.page) + n).toString();
        // Navigate with new filters
        navigate({
            pathname: "/category",
            search: createSearchParams(filters).toString(),
        });
        // Calculate scroll position of top of pagination section
        let obj = document.querySelector(".categoryListingsHead");
        let objTop = 0;
        if (obj.offsetParent) {
            do {
                objTop += obj.offsetTop;
            } while ((obj = obj.offsetParent));
        }
        // Scroll page to top of pagination section
        window.scrollTo(0, objTop - 50);
    }

    return (
        <div className="categoryPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                <div className="head">
                    {/* Category Description */}
                    <div className="info">
                        <h1 data-testid="categoryName">{category.name}</h1>
                        <p data-testid="categoryDescription">{category.description}</p>
                    </div>
                    {/* Category Image */}
                    <div className="image">
                        {category.image_encoded ? (
                            <img data-testid="categoryImage" src={`data:image/jpg;base64,${category.image_encoded}`} alt={category.name} />
                        ) : (
                            <div>No image available</div>
                        )}
                    </div>
                </div>
                {/* Category Sections */}
                <BestSellers />
                <NewListings />
                <CategoryListings />
                {/* Pagination Controls */}
                <div className="pagination">
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon" />&ensp;Previous</Button>
                    <Button style={{marginLeft: "25px"}} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos
                        className="icon" /></Button>
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default Category;

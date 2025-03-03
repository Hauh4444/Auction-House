// External Libraries
import { useState, useEffect } from "react";
import { useNavigate, createSearchParams } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";

// Stylesheets
import "./CategoriesPopup.scss";

/**
 * CategoriesPopup component fetches a list of categories from an API and displays them as buttons.
 * Clicking a category button navigates to a category page with the selected category as a query parameter.
 *
 * Features:
 * - Fetches category data from "http://127.0.0.1:5000/api/categories" when mounted.
 * - Stores the fetched categories in state.
 * - Generates a button for each category, which navigates to the corresponding category page.
 *
 * @returns {JSX.Element} A popup displaying category buttons.
 */
const CategoriesPopup = () => {
    // State to store the fetched categories
    const [categories, setCategories] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch categories from the backend API when the component mounts
        axios.get("http://127.0.0.1:5000/api/categories", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => {
                // Update state with the fetched categories
                setCategories(res.data.categories);
            })
            .catch(err => {
                // Log any errors that occur during the request
                console.log(err);
            });
    }, []); // Empty dependency array ensures this effect runs only once

    /**
     * Handles navigation to the selected category page.
     * Replaces spaces with hyphens and '&' with 'and' for cleaner URLs.
     *
     * @param {string} category - The category name to navigate to.
     */
    function navigateToCategory(category) {
        navigate({
            pathname: "/category",
            search: createSearchParams({
                c: category.replace(/\s/g, "-").replace(/&/g, "and") // Format category name for URL
            }).toString(),
        });
    }

    return (
        <div className="categoriesPopup">
            {/* Map over the categories and create a button for each */}
            {categories.map((category, index) => (
                <div
                    style={{ width: "25%", display: "inline-block", textAlign: "center" }}
                    key={index}
                >
                    <Button
                        className="categoryBtn"
                        onClick={() => navigateToCategory(category)}
                        key={index}
                    >
                        {category}
                    </Button>
                </div>
            ))}
        </div>
    );
}

export default CategoriesPopup;

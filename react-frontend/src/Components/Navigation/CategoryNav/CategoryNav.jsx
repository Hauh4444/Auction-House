// External Libraries
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";

// Stylesheets
import "./CategoryNav.scss";

/**
 * CategoryNav component displays a list of product categories and provides navigation functionality.
 *
 * Features:
 * - Fetches category data from an API on component mount.
 * - Displays categories in a popup or a grid layout depending on the current page.
 * - Allows users to navigate to specific category pages using query parameters.
 *
 * @returns {JSX.Element} A section displaying categories with navigation buttons.
 */
const CategoryNav = () => {
    const navigate = useNavigate(); // To navigate between pages
    const location = useLocation(); // Hook to access the current location (URL)

    const [categories, setCategories] = useState([]); // State to store fetched categories

    // Fetch categories from API on component mount
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/categories/", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => setCategories(res.data.categories)) // Set the fetched categories into the state
            .catch(err => console.log(err)); // Log errors if any
    }, []); // Empty dependency array ensures the request runs once when the component mounts

    // Function to navigate to the selected category page
    const navigateToCategory = (id) => {
        // Close the categories navigation if on a page other than home
        if (location.pathname !== "/") {
            document.querySelector(".categoryNav").style.maxHeight = "0";
        }
        navigate(`/category?category_id=${id}&page=1`); // Navigate to the category page with the category ID and page number
    }

    return (
        <>
            {/* Check if the current page is not the homepage */}
            {location.pathname !== "/" ? (
                <nav className="categoryNav" data-testid="categoryNav">
                    {categories.map((category, index) => (
                        <div className="categoryContainer" key={index}>
                            <Button className="categoryBtn" onClick={() => navigateToCategory(category.category_id)}
                                    key={index}>
                                {category.name} {/* Display category name */}
                            </Button>
                        </div>
                    ))}
                </nav>
            ) : (
                <div className="categoryList" data-testid="categoryList">
                    {categories.map((category, index) => (
                        <div className="category" key={index}>
                            <div className="image">
                                {/* Check if category has an image, if yes, display it, otherwise show a fallback */}
                                {category.image_encoded ? (
                                    <img src={`data:image/jpg;base64,${category.image_encoded}`} alt={category.name} />
                                ) : (
                                    <div>No image available</div>
                                )}
                            </div>
                            <div className="categoryBtn">
                                <Button className="btn" onClick={() => navigateToCategory(category.category_id)}
                                        key={index}>
                                    {category.name} {/* Display category name */}
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </>
    );
}

export default CategoryNav;

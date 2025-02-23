import { useState, useEffect } from "react";
import { useNavigate, createSearchParams } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
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
    const [categories, setCategories] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/categories", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => {
                setCategories(res.data.categories);
            })
            .catch(err => {
                console.log(err);
            });
    }, []); // Empty dependency array to ensure it runs only once when the component is mounted

    function navigateToCategory(category) {
        navigate({
            pathname: "/category",
            search: createSearchParams({
                c: category.replace(/\s/g, "-").replace(/&/g, "and")
            }).toString(),
        });
    }

    return (
        <div className="categoriesPopup">
            {categories.map((category, index) => (
                <div style={{width: "25%", display: "inline-block", textAlign: "center"}} key={index}>
                    <Button className="categoryBtn" onClick={() => navigateToCategory(category)} key={index}>
                        {category}
                    </Button>
                </div>
            ))}
        </div>
    )
}

export default CategoriesPopup;
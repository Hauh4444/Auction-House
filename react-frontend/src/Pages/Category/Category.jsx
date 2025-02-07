// External Libraries
import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import CategoryNavigation from "@/Components/CategoryNavigation/CategoryNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import CategoryListings from "@/Components/CategoryListings/CategoryListings";
// Stylesheets
import "./Category.scss";


const Category = () => {
    const [category, setCategory] = useState({}); // State to store category data
    const location = useLocation(); // Accessing the current location object from react-router-dom to read URL parameters

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
    }, [location.search]); // The effect will re-run whenever the 'location.search' (URL search query) changes

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
                        {category.image ? (
                            <img
                                src={"data:image/jpg;base64," + category.image}
                                alt={category.title}
                            />
                        ) : (
                            <div>No image available</div> // Fallback text if there is no image
                        )}
                    </div>
                </div>
                <CategoryNavigation />
                <CategoryListings />
            </div>
            <RightNavigation />
        </div>
    )
}

export default Category;
// External Libraries
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";

// Stylesheets
import "./CategoryNav.scss";

const CategoryNav = () => {
    const [categories, setCategories] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/categories", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => setCategories(res.data))
            .catch(err => console.log(err));
    }, []); // Empty dependency array to ensure it runs only once when the component is mounted

    const navigateToCategory = (id) => {
        if (location.pathname !== "/") {
            document.querySelector(".categoriesPopup").style.maxHeight = "0";
        }
        navigate(`/category?category_id=${id}&page=1`);
    }

    return (
        <>
            {location.pathname !== "/" ? (
                <div className="categoriesPopup">
                    {categories.map((category, index) => (
                        <div style={{width: "25%", display: "inline-block", textAlign: "center"}} key={index}>
                            <Button className="categoryBtn" onClick={() => navigateToCategory(category.category_id)}
                                    key={index}>
                                {category.name}
                            </Button>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="categoriesList">
                    {categories.map((category, index) => (
                        <div className="category" key={index}>
                            <div className="image">
                                {category.image_encoded ? (
                                    <img src={`data:image/jpg;base64,${category.image_encoded}`} alt={category.title} />
                                ) : (
                                    <div>No image available</div>
                                )}
                            </div>
                            <div className="categoryBtn">
                                <Button className="btn" onClick={() => navigateToCategory(category.category_id)}
                                        key={index}>
                                    {category.name}
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        < />
    )
}

export default CategoryNav;
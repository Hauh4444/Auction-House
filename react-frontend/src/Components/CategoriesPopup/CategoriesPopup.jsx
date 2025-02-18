import { useState, useEffect } from "react";
import { useNavigate, createSearchParams } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
import "./CategoriesPopup.scss"

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
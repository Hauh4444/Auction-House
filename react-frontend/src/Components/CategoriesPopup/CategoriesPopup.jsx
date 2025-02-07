// External Libraries
import { useState, useEffect } from "react";
import { useNavigate, createSearchParams } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
// Stylesheets
import "./CategoriesPopup.scss";

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
                setCategories(res.data);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    function navigateToCategory(id) {
        document.querySelector(".categoriesPopup").style.maxHeight = "0";
        navigate({
            pathname: "/category",
            search: createSearchParams({
                category: id,
                page: 1,
            }).toString(),
        });
    }

    return (
        <div className="categoriesPopup">
            {categories.map((category, index) => (
                <div style={{width: "25%", display: "inline-block", textAlign: "center"}} key={index}>
                    <Button className="categoryBtn" onClick={() => navigateToCategory(category.category_id)} key={index}>
                        {category.name}
                    </Button>
                </div>
            ))}
        </div>
    )
}

export default CategoriesPopup;
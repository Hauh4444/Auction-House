import { useState, useEffect } from 'react';
import { useNavigate, createSearchParams } from 'react-router-dom';
import { Button } from "@mui/material";
import axios from 'axios';
import "./CategoryNavigation.scss"

const CategoryNavigation = () => {
    const [categories, setCategories] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/categories', {
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(res => {
                setCategories(res.data.categories);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    function navigateToCategory(category) {
        navigate({
            pathname: '/categories',
            search: createSearchParams({
                c: category.replace(/\s/g, '-').replace(/&/g, 'and')
            }).toString(),
        });
    }

    return (
        <div className="categoryNav">
            {categories.map((category, index) => (
                <div style={{width: "33%", display: "inline-block", textAlign: "center"}}>
                    <Button className="navBtn" onClick={() => navigateToCategory(category)} key={index}>
                        {category}
                    </Button>
                </div>
            ))}
        </div>
    )
}

export default CategoryNavigation;
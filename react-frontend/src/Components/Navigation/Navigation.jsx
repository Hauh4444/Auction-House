import { useState, useEffect } from 'react';
import { useNavigate, createSearchParams } from 'react-router-dom';
import { Button } from "@mui/material";
import axios from 'axios';
import './Navigation.scss';

const Navigation = () => {
    let [categories, setCategories] = useState([]);
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
        <nav className="navBar">
            {categories.map((category, index) => (
                <Button className="navBtn" onClick={() => navigateToCategory(category)} key={index}>
                    {category}
                </Button>
            ))}
        </nav>
    )
};

export default Navigation;
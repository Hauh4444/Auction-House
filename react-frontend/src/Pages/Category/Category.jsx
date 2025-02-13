// External Libraries
import {useEffect, useState} from "react";
import {createSearchParams, useLocation, useNavigate} from "react-router-dom";
import {MdArrowBackIosNew, MdArrowForwardIos} from "react-icons/md";
import {Button} from "@mui/material";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/Right/RightNav.jsx";
import CategoryListings from "@/Components/Category/Listings/CategoryListings.jsx";
import BestSellers from "@/Components/Category/BestSellers/BestSellers";
import NewListings from "@/Components/Category/NewListings/NewListings";
// Stylesheets
import "./Category.scss";

const Category = () => {
    const [category, setCategory] = useState({});

    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        axios.get(`http://127.0.0.1:5000/api/categories/${filters.category_id}`, {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => setCategory(res.data))
            .catch(err => console.log(err));
    }, [location.search]);

    function pagination(n) {
        filters.page = parseInt(filters.page) + n;
        navigate({
            pathname: "/category",
            search: createSearchParams(filters).toString(),
        });
        let obj = document.querySelector(".categoryListingsHead");
        let objTop = 0;
        if (obj.offsetParent) {
            do {
                objTop += obj.offsetTop;
            } while ((obj = obj.offsetParent));
        }
        window.scrollTo(0, objTop - 50);
    }

    return (
        <div className="categoryPage">
            <div className="mainPage">
                <Header/>
                <div className="head">
                    <div className="info">
                        <h1>{category.name}</h1>
                        <p>{category.description}</p>
                    </div>
                    <div className="image">
                        {category.image_encoded ? (
                            <img src={`data:image/jpg;base64,${category.image_encoded}`} alt={category.title}/>
                        ) : (
                            <div>No image available</div>
                        )}
                    </div>
                </div>
                <BestSellers/>
                <NewListings/>
                <CategoryListings/>
                <div className="pagination">
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon"/>&ensp;Previous</Button>
                    <Button style={{marginLeft: "25px"}} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos
                        className="icon"/></Button>
                </div>
            </div>
            <RightNav/>
        </div>
    );
};

export default Category;
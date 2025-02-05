<<<<<<< HEAD
// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation";
// Stylesheets
import "@/Components/Navigation/Navigation.scss";

const HomeNavigation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            const condition = filters.nav ? btn.classList.contains(filters.nav) : btn.classList.contains("home");
            btn.classList.toggle("selected", condition);
        });
    }, [location.search]);

    const handleNavClick = (e, navBtnClass) => {
        toggleNav(e);
        filters.nav = navBtnClass;
        navigate({
            pathname: "/",
            search: createSearchParams(filters).toString(),
        });
    };

    return (
        <div className="homeNav">
            {["home", "orders", "lists", "deals", "sell"].map((navBtnClass, index) => (
                <Button
                    className={`navBtn ${navBtnClass}`}
                    onClick={(e) => {handleNavClick(e, navBtnClass)}}
                    key={index}
                >
                    {navBtnClass.charAt(0).toUpperCase() + navBtnClass.slice(1).replace(/([A-Z])/g, ' $1')}
                </Button>
            ))}
        </div>
    );
};

export default HomeNavigation;
=======
import CategoriesPopup from "@/Components/CategoriesPopup/CategoriesPopup.jsx";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";
import { toggleNav } from "@/Components/Navigation/Navigation.jsx"
import "@/Components/Navigation/Navigation.scss"

const HomeNavigation = () => {

    function toggleCategoriesDisplay() {
        let element = document.querySelector(".categoriesPopup");
        if (["0px", ""].includes(element.style.maxHeight)) {
            element.style.maxHeight = "100%";
        }
        else {
            element.style.maxHeight = "0";
        }
    }

    return (
        <>
            <div className="homeNav">
                <Button className="navBtn selected" onClick={(e) => {toggleNav(e)}}>
                    Home
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    My Orders
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    My Lists
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    Deals
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    Sell
                </Button>
                <Button className="navBtn categoriesBtn" onClick={toggleCategoriesDisplay}>
                    Categories&ensp;<BsGrid3X3GapFill className="icon" />
                </Button>
            </div>
            <CategoriesPopup />
        </>
    )
}

export default HomeNavigation;
>>>>>>> 9d377c2 (update)

// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation.js";
// Stylesheets
import "@/Components/Navigation/Navigation.scss";

const CategoryNavigation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const filters = Object.fromEntries(queryParams.entries());

    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            const isSelected = filters.nav ? btn.classList.contains(filters.nav) : btn.classList.contains("best");
            btn.classList.toggle("selected", isSelected);
        });
    }, [location.search]);

    const handleNavClick = (e, navBtnClass) => {
        toggleNav(e);
        filters.nav = navBtnClass;
        navigate({
            pathname: "/category",
            search: createSearchParams(filters).toString(),
        });
    };

    return (
        <div className="categoryNav">
            {["best", "new"].map((navBtnClass, index) => (
                <Button
                    className={`navBtn ${navBtnClass}`}
                    onClick={(e) => {handleNavClick(e, navBtnClass)}}
                    key={index}
                >
                    {navBtnClass === "best" ? "Best Sellers": "New"}
                </Button>
            ))}
        </div>
    );
};

export default CategoryNavigation;

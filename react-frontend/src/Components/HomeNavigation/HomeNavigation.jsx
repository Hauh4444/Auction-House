// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation.js";
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

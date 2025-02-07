// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdFilterAlt } from "react-icons/md";
import { Button } from "@mui/material";
// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation.js";
// Stylesheets
import "@/Components/Navigation/Navigation.scss";

const SearchNavigation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const filters = Object.fromEntries(queryParams.entries());

    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            const condition = filters.nav ? btn.classList.contains(filters.nav) : btn.classList.contains("best");
            btn.classList.toggle("selected", condition);
        });
    }, [location.search]);

    function handleNavClick(e, newFilters) {
        toggleNav(e);
        Object.entries(newFilters).forEach(([key, value]) => {
            if (value === null) delete filters[key];
            else filters[key] = value;
        });
        ["best", "deals", "all"].forEach(c => e.target.classList.contains(c) && (filters.nav = c));
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });
    }

    return (
        <div className="searchNav">
            <Button className="navBtn best" onClick={(e) => {
                handleNavClick(e, {page: null, start: 1, end: 10, other: null});
            }}>
                Best Results
            </Button>
            <Button className="navBtn deals" onClick={(e) => {
                handleNavClick(e, {page: null, start: null, end: null, other: "best deals"});
            }}>
                Best Deals
            </Button>
            <Button className="navBtn all" onClick={(e) => {
                handleNavClick(e, {page: 1, start: null, end: null, other: null});
            }}>
                View All
            </Button>
            <Button className="navBtn sortBtn">
                Filters&ensp;<MdFilterAlt className="icon" />
            </Button>
        </div>
    )
}

export default SearchNavigation;
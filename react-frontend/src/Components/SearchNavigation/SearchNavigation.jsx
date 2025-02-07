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
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            const condition = filters.nav ? btn.classList.contains(filters.nav) : btn.classList.contains("best-sellers");
            btn.classList.toggle("selected", condition);
        });
    }, [location.search]);

    function handleNavClick(e, newFilters) {
        toggleNav(e);
        Object.entries(newFilters).forEach(([key, value]) => {
            if (value === null) delete filters[key];
            else filters[key] = value;
        });
        ["best-results", "best-sellers", "new", "view-all"].forEach(c => e.target.classList.contains(c) && (filters.nav = c));
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });
    }

    return (
        <div className="searchNav">
            <Button className="navBtn best-results" onClick={(e) => {
                handleNavClick(e, {page: null, start: 1, end: 10, nav: null});
            }}>
                Best Results
            </Button>
            <Button className="navBtn best-sellers" onClick={(e) => {
                handleNavClick(e, {page: null, start: null, end: null, nav: "best-sellers"});
            }}>
                Best Sellers
            </Button>
            <Button className="navBtn new" onClick={(e) => {
                handleNavClick(e, {page: null, start: null, end: null, nav: "new"});
            }}>
                New
            </Button>
            <Button className="navBtn view-all" onClick={(e) => {
                handleNavClick(e, {page: 1, start: null, end: null, nav: null});
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
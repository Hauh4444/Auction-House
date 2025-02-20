// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdFilterAlt } from "react-icons/md";
import { Button } from "@mui/material";

// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation/Navigation";
import Popup from "@/Components/Filters/Popup/Popup";

// Stylesheets
import "@/Components/Navigation/Navigation/Navigation.scss";

/**
 * SearchNav Component
 *
 * This component provides a navigation bar for the search page,
 * allowing users to filter search results based on different categories.
 * It includes buttons for "Best Results," "Best Sellers," "New,"
 * and "View All," enabling users to navigate between different
 * types of search results. The component also features a button to
 * toggle the visibility of a filter popup, which allows users to
 * apply additional filters to their search.
 *
 * The component updates the URL query parameters based on the
 * selected navigation option and maintains the selected state
 * for the navigation buttons to enhance user experience.
 *
 * @returns {JSX.Element} A navigation component for the search page
 *                        with buttons for different result categories
 *                        and a filter popup.
 */
const SearchNav = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            let condition;
            if (filters.nav) {
                condition = btn.classList.contains(filters.nav);
            } else {
                condition = btn.classList.contains("best-sellers");
            }
            btn.classList.toggle("selected", condition);
        });
    }, [location.search]);

    function handleNavClick(e, newFilters) {
        toggleNav(e);
        Object.entries(newFilters).forEach(([key, value]) => {
            if (value === null) {
                delete filters[key];
            } else {
                filters[key] = value;
            }
        });
        ["best-results", "best-sellers", "new", "view-all"].forEach(c => e.target.classList.contains(c) && (filters.nav = c));
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });
    }

    function toggleFiltersDisplay() {
        const element = document.querySelector(".filtersPopup");
        if (element.style.maxHeight === "0px" || element.style.maxHeight === "") {
            element.style.maxHeight = "100%";
        } else {
            element.style.maxHeight = "0";
        }
    }

    return (
        <>
            <div className="searchNav">
                <Button className="navBtn best-results" onClick={(e) => {
                    handleNavClick(e, {page: null, start: 0, range: 10, nav: null});
                    document.querySelector(".filtersPopup").style.maxHeight = "0px";
                }}>
                    Best Results
                </Button>
                <Button className="navBtn best-sellers" onClick={(e) => {
                    handleNavClick(e, {page: null, start: null, range: null, nav: "best-sellers"});
                    document.querySelector(".filtersPopup").style.maxHeight = "0px";
                }}>
                    Best Sellers
                </Button>
                <Button className="navBtn new" onClick={(e) => {
                    handleNavClick(e, {page: null, start: null, range: null, nav: "new"});
                    document.querySelector(".filtersPopup").style.maxHeight = "0px";
                }}>
                    New
                </Button>
                <Button className="navBtn view-all" onClick={(e) => {
                    handleNavClick(e, {page: 1, start: null, range: null, nav: null});
                    document.querySelector(".filtersPopup").style.maxHeight = "0px";
                }}>
                    View All
                </Button>
                <Button className="navBtn filtersBtn" onClick={toggleFiltersDisplay}>
                    Filters&ensp;<MdFilterAlt className="icon" />
                </Button>
            </div>
            <Popup />
        < />
    )
}

export default SearchNav;
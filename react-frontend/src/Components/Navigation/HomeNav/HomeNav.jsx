// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation/Navigation";

// Stylesheets
import "@/Components/Navigation/Navigation/Navigation.scss";

/**
 * HomeNav component provides a navigation bar for the home page, allowing users to switch between different sections.
 *
 * Features:
 * - Updates the URL query parameters based on the selected navigation button.
 * - Highlights the currently selected navigation button based on the URL state.
 * - Uses the `toggleNav` function to handle navigation toggling.
 *
 * @returns {JSX.Element} A navigation bar with buttons for Home, Orders, Lists, Deals, and Sell.
 */
const HomeNav = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            let condition;
            if (filters.nav) {
                condition = btn.classList.contains(filters.nav);
            } else {
                condition = btn.classList.contains("home");
            }
            btn.classList.toggle("selected", condition);
        });
    }, [location.search]);

    const handleNavClick = (e, navBtnClass) => {
        toggleNav(e);
        if (navBtnClass !== "home") {
            filters.nav = navBtnClass;
        } else {
            delete filters.nav;
        }
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
                    onClick={(e) => {
                        handleNavClick(e, navBtnClass)
                    }}
                    key={index}
                >
                    {navBtnClass.charAt(0).toUpperCase() + navBtnClass.slice(1).replace(/([A-Z])/g, ' $1')}
                </Button>
            ))}
        </div>
    );
};

export default HomeNav;

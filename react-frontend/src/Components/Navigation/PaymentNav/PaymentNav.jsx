// External Libraries
import { useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

// Internal Modules
import toggleNav from "@/Components/Navigation/Navigation/Navigation";

// Stylesheets
import "@/Components/Navigation/Navigation/Navigation.scss";

const HistoryNav = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Parse query parameters

    // Effect to handle the active navigation button based on current filters
    useEffect(() => {
        document.querySelectorAll(".navBtn").forEach(btn => {
            let condition;
            if (filters.nav) {
                condition = btn.classList.contains(filters.nav); // Check if button matches the current filter
            } else {
                condition = btn.classList.contains("transactions");
            }
            btn.classList.toggle("selected", condition); // Toggle "selected" class based on condition
        });
    }, [location.search]); // Run effect when URL search params change

    // Handle click on navigation buttons, update filters and navigate
    function handleNavClick(e, nav) {
        toggleNav(e); // Toggle navigation state
        filters.nav = nav;
        // Navigate with updated query parameters
        navigate({
            pathname: "/user/payment-info",
            search: createSearchParams(filters).toString(),
        });
    }

    return (
        <>
            <nav className="paymentNav">
                {["transactions", "payments"].map((item, index) => (
                    <Button className={ `navBtn ${ item  }`} data-testid={ `${ item  }Btn`} key={ index } onClick={(e) => {
                        handleNavClick(e, item);
                    }}>
                        { String(item).charAt(0).toUpperCase() + String(item).slice(1) }
                    </Button>
                ))}
            </nav>
        </>
    );
}

export default HistoryNav;

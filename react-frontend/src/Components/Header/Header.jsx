// External Libraries
import { useLocation, useNavigate } from "react-router-dom";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";

// Internal Modules
import SearchBar from "@/Components/Navigation/SearchBar/SearchBar";
import CategoryNav from "@/Components/Navigation/CategoryNav/CategoryNav";

// Stylesheets
import "./Header.scss";

/**
 * Header component renders the top navigation bar of the application.
 * It includes navigation buttons, a search bar, and category toggling functionality.
 *
 * Features:
 * - Navigation buttons for Home, Shop All, About, and Contact pages.
 * - A "Categories" button that toggles the display of a category navigation (except on the homepage).
 * - A search bar component (`SearchBar`).
 * - A category navigation bar (`CategoryNav`), displayed on all pages except the homepage.
 *
 * @returns {JSX.Element} The header section with navigation and search functionalities.
 */
const Header = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)

    /**
     * Toggles the visibility of the category navigation.
     * Adjusts the `maxHeight` CSS property to show or hide the popup.
     */
    function toggleCategoriesDisplay() {
        const element = document.querySelector(".categoryNav");
        if (element.style.maxHeight === "0px" || element.style.maxHeight === "") {
            element.style.maxHeight = "100%"; // Expands the popup
        } else {
            element.style.maxHeight = "0"; // Collapses the popup
        }
    }

    return (
        <>
            <div className="header">
                <div className="headNav">
                    {/* Navigation Buttons */}
                    <Button className="btn" onClick={() => navigate("/")}>
                        Home
                    </Button>
                    <Button className="btn" onClick={() => navigate("/search")}>
                        Shop All
                    </Button>
                    <Button className="btn" onClick={() => navigate("/about")}>
                        About
                    </Button>
                    <Button className="btn" onClick={() => navigate("/contact")}>
                        Contact
                    </Button>

                    {/* Categories Button (Hidden on Homepage) */}
                    {location.pathname !== "/" && (
                        <Button className="btn categoriesBtn" onClick={toggleCategoriesDisplay}>
                            Categories&ensp;<BsGrid3X3GapFill className="icon" />
                        </Button>
                    )}
                </div>

                {/* Search SearchBar Component */}
                <SearchBar />
            </div>

            {/* Category Navigation (Hidden on Homepage) */}
            {location.pathname !== "/" && <CategoryNav />}
        </>
    );
}

export default Header;

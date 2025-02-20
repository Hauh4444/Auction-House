// External Libraries
import { useLocation, useNavigate } from "react-router-dom";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";

// Internal Modules
import Bar from "@/Components/Search/Bar/Bar";
import CategoryNav from "@/Components/Navigation/CategoryNav/CategoryNav";

// Stylesheets
import "./Header.scss";

/**
 * Header component renders the top navigation bar of the application.
 * It includes navigation buttons, a search bar, and category toggling functionality.
 *
 * Features:
 * - Navigation buttons for Home, Shop All, About, and Contact pages.
 * - A "Categories" button that toggles the display of a categories popup (except on the homepage).
 * - A search bar component (`Bar`).
 * - A category navigation bar (`CategoryNav`), displayed on all pages except the homepage.
 *
 * @returns {JSX.Element} The header section with navigation and search functionalities.
 */
const Header = () => {
    const navigate = useNavigate();
    const location = useLocation();

    function toggleCategoriesDisplay() {
        const element = document.querySelector(".categoriesPopup");
        if (element.style.maxHeight === "0px" || element.style.maxHeight === "") {
            element.style.maxHeight = "100%";
        } else {
            element.style.maxHeight = "0";
        }
    }

    return (
        <>
            <div className="header">
                <div className="headNav">
                    <Button className="btn" onClick={() => {
                        navigate("/")
                    }}>

                        Home
                    </Button>
                    <Button className="btn" onClick={() => {
                        navigate("/search")
                    }}>
                        Shop All
                    </Button>
                    <Button className="btn" onClick={() => {
                        navigate("/about")
                    }}>
                        About
                    </Button>
                    <Button className="btn" onClick={() => {
                        navigate("/contact")
                    }}>
                        Contact
                    </Button>
                    {location.pathname !== "/" && (
                        <Button className="btn categoriesBtn" onClick={toggleCategoriesDisplay}>
                            Categories&ensp;<BsGrid3X3GapFill className="icon" />
                        </Button>
                    )}
                </div>
                <Bar />
            </div>
            {location.pathname !== "/" && (
                <CategoryNav />
            )}
        < />
    )
}

export default Header;
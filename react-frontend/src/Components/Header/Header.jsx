// External Libraries
import { useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { FaSearch } from "react-icons/fa";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button, TextField } from "@mui/material";

// Internal Modules
import CategoryNav from "@/Components/Navigation/CategoryNav/CategoryNav";

// Stylesheets
import "./Header.scss";

// Custom Variables
import { variables } from "@/assets/variables.modules";

/**
 * Header component renders the top navigation bar of the application.
 * It includes navigation buttons, a search bar, and category toggling functionality.
 *
 * Features:
 * - Navigation buttons for Home, Shop All, About, and Contact pages.
 * - A "Categories" button that toggles the display of a category navigation (except on the homepage).
 * - Search bar captures user input for search queries.
 * - Search bar redirects to the home page if the input is empty.
 * - Search bar redirects to the search results page with query parameters based on user input.
 * - Search bar supports both button click and Enter key for initiating search.
 * - A category navigation bar (`CategoryNav`), displayed on all pages except the homepage.
 *
 * @returns { JSX.Element } The header section with navigation and search functionalities.
 */
const Header = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)

    const [query, setQuery] = useState(""); // State to hold the search query input

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

    // Function to navigate to the search results or home page based on query input
    function navigateSearch() {
        // If the search input is empty, navigate to home page with default view
        if (query === "") {
            navigate("/");
        } else {
            // Otherwise, navigate to the search results page with the query and other filters
            navigate({
                pathname: "/search",
                search: createSearchParams({
                    query: query, // User's search query
                    start: "0", // Start pagination from the first page
                    range: "10", // Limit results to 10
                    nav: "best-results", // Default to "best-results" view
                }).toString(),
            });
        }
    }

    return (
        <>
            <div className="header">
                <div className="headNav">
                    { /* Navigation Buttons */ }
                    <Button className="btn" onClick={ () => navigate("/") }>
                        Home
                    </Button>
                    <Button className="btn" onClick={ () => navigate("/search") }>
                        Shop All
                    </Button>
                    <Button className="btn" onClick={ () => navigate("/about") }>
                        About
                    </Button>
                    <Button className="btn" onClick={ () => navigate("/contact") }>
                        Contact
                    </Button>

                    { /* Categories Button (Hidden on Homepage) */ }
                    {location.pathname !== "/" && (
                        <Button className="btn categoriesBtn" onClick={ toggleCategoriesDisplay }>
                            Categories&ensp;<BsGrid3X3GapFill className="icon" />
                        </Button>
                    )}
                </div>

                <div className="searchBar">
                    { /* Input field for the search query */ }
                    <TextField
                        className="input"
                        value={ query } // Bind the input value to the query state
                        placeholder="Search" // Placeholder text
                        onChange={ (e) => setQuery(e.target.value) } // Update query on input change
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                navigateSearch() // Trigger search when Enter key is pressed
                            }
                        }}
                        variant="outlined"
                        size="small"
                        type="text"
                        sx={{
                            "& .MuiOutlinedInput-root": {
                                "& fieldset": {
                                    border: `none`, // Remove the border around the input field
                                },
                            },
                        }}
                    />
                    { /* Search button with an icon */ }
                    <Button className="btn" data-testid="searchBtn" onClick={ navigateSearch }>
                        <svg width="0" height="0">
                            <defs>
                                { /* Gradient definition for the search icon */ }
                                <linearGradient id="gradient" x1="0%" y1="50%" x2="100%" y2="50%">
                                    <stop stopColor={ variables.accentColor1 } offset="0%" />
                                    <stop stopColor={ variables.accentColor2 } offset="100%" />
                                </linearGradient>
                            </defs>
                        </svg>
                        { /* Search icon with applied gradient color */ }
                        <FaSearch className="icon" style={ { fill: "url(#gradient)" } } />
                    </Button>
                </div>
            </div>

            { /* Category Navigation (Hidden on Homepage) */ }
            { location.pathname !== "/" && <CategoryNav /> }
        </>
    );
}

export default Header;

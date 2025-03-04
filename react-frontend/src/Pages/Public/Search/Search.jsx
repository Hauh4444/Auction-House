// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import SearchNav from "@/Components/Navigation/SearchNav/SearchNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import SearchListings from "@/Components/Search/SearchListings/SearchListings";

/**
 * Search Component
 *
 * This component handles search functionality and displays search results.
 * It includes pagination support for viewing multiple pages of results.
 *
 * Features:
 * - Retrieves query parameters from the URL.
 * - Displays search results using `SearchListings`.
 * - Provides pagination buttons when 'view-all' mode is enabled.
 *
 * @returns {JSX.Element} The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
 */
const Search = () => {
    // State to store the pagination buttons
    const [paginationButtons, setPaginationButtons] = useState(null);

    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    // Extract query parameters from URL
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {
        
        // Display pagination buttons if "view-all" navigation is selected
        if (filters.nav === "view-all") {
            setPaginationButtons(
                // Pagination buttons
                <div className="pagination">
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon" />&ensp;Previous</Button>
                    <Button style={{marginLeft: "25px"}} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos
                        className="icon" /></Button>
                </div>
            );
        } else {
            // Remove pagination buttons if other navigation is selected
            setPaginationButtons(null);
        }
    }, [location.search]);

    /**
     * Handles pagination for search results.
     * Adjusts the `page` parameter in the URL and reloads results.
     *
     * @param {number} n - Increment or decrement for pagination.
     */
    function pagination(n) {
        // Update URL filter
        filters.page = (parseInt(filters.page) + n).toString();
        // Navigate with new filters
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });
        // Scroll to top of page
        window.scrollTo(0, 0);
    }

    return (
        <div className="searchPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                {/* Search Navigation */}
                <SearchNav />
                {/* Search Listings */}
                <SearchListings />
                {/* Pagination Controls */}
                {paginationButtons}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default Search;

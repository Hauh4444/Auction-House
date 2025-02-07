// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { Button } from "@mui/material";
// Internal Modules
import Header from "@/Components/Header/Header";
import SearchNavigation from "@/Components/SearchNavigation/SearchNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import SearchListings from "@/Components/SearchListings/SearchListings";
// Stylesheets
import "./Search.scss"; // Importing styles for this page


const Search = () => {
    const navigate = useNavigate(); // Hook for navigation
    const location = useLocation(); // Hook to access the current location (URL)
    const queryParams = new URLSearchParams(location.search); // Parse query parameters from the URL
    const filters = Object.fromEntries(queryParams.entries()); // Convert query parameters to an object for easier use
    const [paginationButtons, setPaginationButtons] = useState(null); // State to manage pagination buttons visibility

    // useEffect to control pagination buttons visibility based on filter changes
    useEffect(() => {
        // Check if the filter 'nav' is set to 'all', to show pagination controls
        if (filters.nav === "view-all") {
            // Set pagination buttons for 'previous' and 'next' navigation
            setPaginationButtons(
                <div className="pagination">
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon" />&ensp;Previous</Button>
                    <Button style={{ marginLeft: "25px" }} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos className="icon" /></Button>
                </div>
            );
        }
        else {
            // If not in 'all' hide pagination buttons
            setPaginationButtons(null);
        }
    }, [location.search]) // Dependency on location.search to re-run whenever the search parameters change

    // Function to handle pagination
    function pagination(n) {
        // Increment or decrement the page number (p) in filters
        filters.page = parseInt(filters.page) + n;
        // Update the URL with the new filters (this causes a re-render)
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(), // Convert filters object to query string
        });
        window.scrollTo(0, 0);
    }

    return (
        <div className="searchPage">
            <div className="mainPage">
                <Header />
                <SearchNavigation />
                <SearchListings />
                {/* Render pagination buttons only when 'paginationButtons' is not null */}
                {paginationButtons}
            </div>
            <RightNavigation />
        </div>
    )
}

export default Search;
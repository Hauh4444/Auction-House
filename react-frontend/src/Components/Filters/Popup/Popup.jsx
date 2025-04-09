// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { FormControl, TextField, InputLabel, MenuItem, Select } from "@mui/material";
import axios from "axios";

// Stylesheets
import "./Popup.scss";

/**
 * Popup Component
 *
 * This component renders a filter popup that allows users to refine
 * their search results based on various criteria such as sorting options,
 * categories, listing types, and price ranges. It fetches the list of
 * categories from the API on mount and updates the URL parameters
 * dynamically when filters are applied.
 *
 * Features:
 * - A dropdown to select sorting criteria (e.g., relevance, date, price).
 * - A dropdown to select categories fetched from an API.
 * - A dropdown to select the type of listing (e.g., auction, buy now).
 * - TextField fields for minimum and maximum price ranges.
 *
 * The filters update the URL query parameters and reflect the current
 * state of the filters applied.
 *
 * @returns { JSX.Element } A filter popup component with various filtering options.
 */
const Popup = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from the URL

    // State variables for managing filter options
    const [sortBy, setSortBy] = useState(filters.sort || "relevance"); // Default to "relevance" if no sort filter is provided
    const [categories, setCategories] = useState([]); // Stores category list fetched from API
    const [category, setCategory] = useState(filters.category_id || "All"); // Default to "All" if no category filter is provided
    const [listingType, setListingType] = useState(filters.listing_type || "All"); // Default to "All" if no listing type filter is provided
    const [minPrice, setMinPrice] = useState(""); // State for minimum price
    const [maxPrice, setMaxPrice] = useState(""); // State for maximum price

    // Effect hook to fetch categories from the API on component mount
    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/categories/`, {
            headers: { "Content-Type": "application/json" },
        })
            .then((res) => setCategories(res.data.categories)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, []); 

    /**
     * Updates the URL search parameters and state when a filter is changed.
     * @param { string } key The name of the filter being updated.
     * @param { string } value The value of the filter.
     */
    function updateFilter(key, value) {
        // Handle sorting filter separately, as it involves both "sort" and "order" parameters
        if (key === "sort") {
            setSortBy(value); // Update the sort criteria
            if (value === "relevance") {
                delete filters.sort; // Remove sort and order if "relevance" is selected
                delete filters.order;
            } else {
                // Define sorting options with respective fields and order
                const sortMap = {
                    "created_at_asc": ["created_at", "asc"],
                    "created_at_desc": ["created_at", "desc"],
                    "current_price_asc": ["current_price", "asc"],
                    "current_price_desc": ["current_price", "desc"],
                    "buy_now_price_asc": ["buy_now_price", "asc"],
                    "buy_now_price_desc": ["buy_now_price", "desc"],
                    "purchases": ["purchases", "desc"],
                    "average_review": ["average_review", "desc"],
                    "total_reviews": ["total_reviews", "desc"]
                };
                // Set sort and order parameters if a valid option is selected
                if (sortMap[value]) {
                    const [sortField, order] = sortMap[value];
                    filters.sort = sortField;
                    filters.order = order;
                } else {
                    delete filters.sort;
                    delete filters.order;
                }
            }
        } else {
            let valueToSet;
            if (value !== "All" && value !== "") {
                valueToSet = value; // Set filter value if not "All" or empty
            } else {
                valueToSet = undefined; // Set filter value to undefined for "All" or empty
            }
            setFilterState(key, valueToSet); // Update the corresponding filter state
            if (valueToSet) {
                filters[key] = valueToSet; // Add to filters if value is set
            } else {
                delete filters[key]; // Remove from filters if value is empty
            }
        }

        // Navigate to the same page with updated search parameters
        navigate({
            pathname: location.pathname,
            search: createSearchParams(filters).toString(),
        });
    }

    /**
     * Updates the state of a specific filter based on the filter type.
     * @param { string } filter The name of the filter being updated.
     * @param { string } value The value of the filter.
     */
    function setFilterState(filter, value) {
        if (filter === "category_id") {
            setCategory(value || "All"); // Update category filter state
        } else if (filter === "listing_type") {
            setListingType(value || "All"); // Update listing type filter state
        } else if (filter === "min_price") {
            setMinPrice(value); // Update minimum price filter state
        } else if (filter === "max_price") {
            setMaxPrice(value); // Update maximum price filter state
        }
    }

    return (
        <div className="filtersPopup" data-testid="filtersPopup">
            <div style={ { height: "20px" } } /> { /* Spacer */ }
            { /* Sort By Filter */ }
            <FormControl size="small">
                <InputLabel id="sortByLabel">Sort By</InputLabel>
                <Select
                    id="sortByInput"
                    labelId="sortByLabel"
                    aria-labelledby="sortByLabel"
                    className="sortBy"
                    value={ sortBy }
                    label="Sort By"
                    onChange={(e) => {
                        updateFilter("sort", e.target.value)
                    }}
                    variant="outlined"
                >
                    <MenuItem value="relevance">Relevance</MenuItem>
                    <MenuItem value="created_at_asc">Oldest</MenuItem>
                    <MenuItem value="created_at_desc">Newest</MenuItem>
                    <MenuItem value="current_price_asc">Current Price Ascending</MenuItem>
                    <MenuItem value="current_price_desc">Current Price Descending</MenuItem>
                    <MenuItem value="buy_now_price_asc">Buy Now Ascending</MenuItem>
                    <MenuItem value="buy_now_price_desc">Buy Now Descending</MenuItem>
                    <MenuItem value="purchases">Purchases</MenuItem>
                    <MenuItem value="average_review">Average Review</MenuItem>
                    <MenuItem value="total_reviews">Total Reviews</MenuItem>
                </Select>
            </FormControl>

            { /* Category Filter */ }
            <FormControl size="small">
                <InputLabel id="categoryLabel">Category</InputLabel>
                <Select
                    id="categoryInput"
                    labelId="categoryLabel"
                    aria-labelledby="categoryLabel"
                    className="category"
                    value={ category }
                    label="Category"
                    onChange={(e) => {
                        updateFilter("category_id", e.target.value)
                    }}
                    variant="outlined"
                >
                    <MenuItem value="All">All</MenuItem>
                    {categories.map((category, index) => (
                        <MenuItem value={ category.category_id } key={ index }>{ category.name }</MenuItem>
                    ))}
                </Select>
            </FormControl>

            { /* Listing Type Filter */ }
            <FormControl size="small">
                <InputLabel id="listingTypeLabel">Listing Type</InputLabel>
                <Select
                    id="listingTypeInput"
                    labelId="listingTypeLabel"
                    aria-labelledby="listingTypeLabel"
                    className="listingType"
                    value={ listingType }
                    label="Listing Type"
                    onChange={(e) => {
                        updateFilter("listing_type", e.target.value)
                    }}
                    variant="outlined"
                >
                    <MenuItem value="All">All</MenuItem>
                    <MenuItem value="auction">Auction</MenuItem>
                    <MenuItem value="buy_now">Buy Now</MenuItem>
                </Select>
            </FormControl>

            { /* Minimum Price Filter */ }
            <TextField
                className="minPrice"
                value={ minPrice }
                label="Min Price"
                type="number"
                onChange={(e) => {
                    updateFilter("min_price", e.target.value)
                }}
                variant="outlined"
            />

            { /* Maximum Price Filter */ }
            <TextField
                className="maxPrice"
                value={ maxPrice }
                label="Max Price"
                type="number"
                onChange={(e) => {
                    updateFilter("max_price", e.target.value)
                }}
                variant="outlined"
            />
        </div>
    )
}

export default Popup;

// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { FormControl, InputLabel, Select, MenuItem, Input } from "@mui/material"
import axios from "axios";
// Stylesheets
import "./FiltersPopup.scss"

const FiltersPopup = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());
    const [sortBy, setSortBy] = useState(filters.sort || "relevance");
    const [categories, setCategories] = useState([]);
    const [category, setCategory] = useState(filters.category_id || "All");
    const [listingType, setListingType] = useState(filters.listing_type || "All");
    const [minPrice, setMinPrice] = useState();
    const [maxPrice, setMaxPrice] = useState();

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/categories", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => setCategories(res.data))
            .catch(err => console.log(err));
    }, []);

    function updateFilter(filter, value) {
        if (filter === "sort") {
            setSortBy(value);
            if (value === "relevance") {
                delete filters.sort;
                delete filters.order;
            } else {
                const sortMap = {
                    "created_at_asc": ["created_at", "asc"],
                    "created_at_desc": ["created_at", "desc"],
                    "starting_price_asc": ["starting_price", "asc"],
                    "starting_price_desc": ["starting_price", "desc"],
                    "buy_now_price_asc": ["buy_now_price", "asc"],
                    "buy_now_price_desc": ["buy_now_price", "desc"],
                    "purchases": ["purchases", "desc"],
                    "average_review": ["average_review", "desc"],
                    "total_reviews": ["total_reviews", "desc"]
                };
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
            const valueToSet = value !== "All" && value !== "" ? value : undefined;
            setFilterState(filter, valueToSet);
            if (valueToSet) {
                filters[filter] = valueToSet;
            } else {
                delete filters[filter];
            }
        }
        navigate({
            pathname: location.pathname,
            search: createSearchParams(filters).toString(),
        });
    }

    function setFilterState(filter, value) {
        if (filter === "category_id") {
            setCategory(value || "All");
        } else if (filter === "listing_type") {
            setListingType(value || "All");
        } else if (filter === "min_price") {
            setMinPrice(value);
        } else if (filter === "max_price") {
            setMaxPrice(value);
        }
    }

    return (
        <div className="filtersPopup">
            <div style={{height: "20px"}}/>
            <FormControl size="small">
                <InputLabel id="sortByLabel">Sort By</InputLabel>
                <Select
                    labelid="sortByLabel"
                    className="sortBy"
                    value={sortBy}
                    label="Sort By"
                    onChange={(e) => {updateFilter("sort", e.target.value)}}
                    variant="outlined"
                >
                    <MenuItem value="relevance">Relevance</MenuItem>
                    <MenuItem value="created_at_asc">Oldest</MenuItem>
                    <MenuItem value="created_at_desc">Newest</MenuItem>
                    <MenuItem value="starting_price_asc">Starting Price Ascending</MenuItem>
                    <MenuItem value="starting_price_desc">Starting Price Descending</MenuItem>
                    <MenuItem value="buy_now_price_asc">Buy Now Ascending</MenuItem>
                    <MenuItem value="buy_now_price_desc">Buy Now Descending</MenuItem>
                    <MenuItem value="purchases">Purchases</MenuItem>
                    <MenuItem value="average_review">Average Review</MenuItem>
                    <MenuItem value="total_reviews">Total Reviews</MenuItem>
                </Select>
            </FormControl>
            <FormControl size="small">
                <InputLabel id="categoryLabel">Category</InputLabel>
                <Select
                    labelid="categoryLabel"
                    className="category"
                    value={category}
                    label="Category"
                    onChange={(e) => {updateFilter("category_id", e.target.value)}}
                    variant="outlined"
                >
                    <MenuItem value="All">All</MenuItem>
                    {categories.map((category, index) => (
                        <MenuItem value={category.category_id} key={index}>{category.name}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            <FormControl size="small">
                <InputLabel id="listingTypeLabel">Listing Type</InputLabel>
                <Select
                    labelid="listingTypeLabel"
                    className="listingType"
                    value={listingType}
                    label="Listing Type"
                    onChange={(e) => {updateFilter("listing_type", e.target.value)}}
                    variant="outlined"
                >
                    <MenuItem value="All">All</MenuItem>
                    <MenuItem value="auction">Auction</MenuItem>
                    <MenuItem value="buy_now">Buy Now</MenuItem>
                </Select>
            </FormControl>
            <FormControl size="small">
                <InputLabel id="minPriceLabel">Min Price</InputLabel>
                <Input
                    labelid="minPriceLabel"
                    className="minPrice"
                    value={minPrice}
                    label="Min Price"
                    type="number"
                    onChange={(e) => {updateFilter("min_price", e.target.value)}}
                    variant="outlined"
                />
            </FormControl>
            <FormControl size="small">
                <InputLabel id="maxPriceLabel">Max Price</InputLabel>
                <Input
                    labelid="maxPriceLabel"
                    className="maxPrice"
                    value={maxPrice}
                    label="Max Price"
                    type="number"
                    onChange={(e) => {updateFilter("max_price", e.target.value)}}
                    variant="outlined"
                />
            </FormControl>
        </div>
    )
}

export default FiltersPopup;
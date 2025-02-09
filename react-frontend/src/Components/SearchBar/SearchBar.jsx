// External Libraries
import { useState } from "react";
import { FaSearch } from "react-icons/fa";
import { useNavigate, createSearchParams } from "react-router-dom";
import { TextField, Button } from "@mui/material";
// Stylesheets
import "./SearchBar.scss";
// Custom Variables
import { variables } from "@/assets/variables.modules.js";

const SearchBar = () => {
    const [query, setQuery] = useState("");
    const navigate = useNavigate();

    function navigateSearch() {
        if (query === "") {
            navigate({
                pathname: "/",
                search: createSearchParams({
                    nav: "view-all",
                }).toString(),
            });
        }
        else {
            navigate({
                pathname: "/search",
                search: createSearchParams({
                    query: query,
                    start: 0,
                    range: 10,
                    nav: "best-results",
                }).toString(),
            });
        }
    }

    return (
        <div className="searchBar">
            <TextField
                className="searchInput"
                value={query}
                placeholder="Search"
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {if (e.key === "Enter") {navigateSearch()}}}
                variant="outlined"
                size="small"
                type="text"
                sx={{
                    "& .MuiOutlinedInput-root": {
                        "& fieldset": {
                            border: `none`,
                        },
                    },
                }}
            />
            <Button className="searchButton" onClick={navigateSearch}>
                <svg width="0" height="0">
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="50%" x2="100%" y2="50%">
                            <stop stopColor={variables.accentColor1} offset="0%" />
                            <stop stopColor={variables.accentColor2} offset="100%" />
                        </linearGradient>
                    </defs>
                </svg>
                <FaSearch className="searchIcon" style={{ fill: "url(#gradient)" }} />
            </Button>
        </div>
    )
}

export default SearchBar;
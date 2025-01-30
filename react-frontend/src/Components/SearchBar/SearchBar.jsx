import { useState } from 'react'
import { FaSearch } from "react-icons/fa";
import { TextField, Button } from "@mui/material";
import './SearchBar.scss'

const SearchBar = () => {
    const [query, setQuery] = useState('');

    const searchChange = (e) => {
        setQuery(e.target.value);
    }

    return (
        <div className="searchBar">
            <TextField
                className="searchInput"
                value={query}
                placeholder="Search"
                onChange={searchChange}
                variant="outlined"
                type="text"
                sx={{
                    '& .MuiOutlinedInput-root': {
                        '& fieldset': {
                            border: `none`,
                        },
                    },
                }}
            />
            <Button className="searchButton">
                <svg width="0" height="0">
                    <linearGradient id="gradient" x1="0%" y1="50%" x2="100%" y2="50%">
                        <stop stopColor="#d53a9d" offset="0%" />
                        <stop stopColor="#743ad5" offset="100%" />
                    </linearGradient>
                </svg>
                <FaSearch className="searchIcon" style={{ fill: "url(#gradient)" }} />
            </Button>
        </div>
    )
}

export default SearchBar;
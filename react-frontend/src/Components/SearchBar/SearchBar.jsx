import { useState } from 'react'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import Button from "@mui/material/Button";

const SearchBar = () => {
    const [query, setQuery] = useState('');
    const category = "All";

    const searchChange = (e) => {
        setQuery(e.target.value);
    }

    const selectChange = (e) => {
        setQuery(e.target.value);
    }

    return (
        <div className="searchBar">
            <Select labelId="categorySelect" id="categorySelect" value={category} label="Category" onChange={selectChange} variant="outlined">
                <MenuItem value="All">All</MenuItem>
                <MenuItem value=""></MenuItem>
            </Select>
            <input className="searchInput" type="text" value={query} onChange={searchChange} placeholder="Search" />
            <Button className="searchBtn"></Button>
        </div>
    )
}

export default SearchBar;
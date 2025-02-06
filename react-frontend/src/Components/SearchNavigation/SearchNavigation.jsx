import { toggleNav } from "@/Components/Navigation/Navigation"
import {createSearchParams, useLocation, useNavigate} from "react-router-dom";
import { MdOutlineSort } from "react-icons/md";
import { Button } from "@mui/material";
import "@/Components/Navigation/Navigation.scss"

const SearchNavigation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const filters = {};
    for (let [key, value] of queryParams.entries()) {
        filters[key] = value;
    }

    function handleNavigate(e, newFilters) {
        toggleNav(e);
        for (let key in newFilters) {
            if (newFilters[key] === null) {
                delete filters[key];
            }
            else {
                filters[key] = newFilters[key];
            }
        }
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });
    }

    return (
        <div className="searchNav">
            <Button className="navBtn selected" onClick={(e) => {handleNavigate(e, {p: null, start: 1, end: 10, o: null})}}>
                Best Results
            </Button>
            <Button className="navBtn" onClick={(e) => {handleNavigate(e, {p: null, start: null, end: null, o: "best deals"})}}>
                Best Deals
            </Button>
            <Button className="navBtn" onClick={(e) => {handleNavigate(e, {p: 1, start: null, end: null, o: null})}}>
                View All
            </Button>
            <Button className="navBtn sortBtn">
                Sort By&ensp; <MdOutlineSort className="icon" />
            </Button>
        </div>
    )
}

export default SearchNavigation;
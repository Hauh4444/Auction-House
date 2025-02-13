// External Libraries
import {useEffect, useState} from "react";
import {createSearchParams, useLocation, useNavigate} from "react-router-dom";
import {MdArrowBackIosNew, MdArrowForwardIos} from "react-icons/md";
import {Button} from "@mui/material";
// Internal Modules
import Header from "@/Components/Header/Header";
import SearchNav from "@/Components/Navigation/Search/SearchNav.jsx";
import RightNav from "@/Components/Navigation/Right/RightNav.jsx";
import SearchListings from "@/Components/Search/Listings/SearchListings.jsx";
// Stylesheets
import "./Search.scss";


const Search = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());
    const [paginationButtons, setPaginationButtons] = useState(null);

    useEffect(() => {
        if (filters.nav === "view-all") {
            setPaginationButtons(
                <div className="pagination">
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon"/>&ensp;Previous</Button>
                    <Button style={{marginLeft: "25px"}} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos
                        className="icon"/></Button>
                </div>
            );
        } else {
            setPaginationButtons(null);
        }
    }, [location.search])

    function pagination(n) {
        filters.page = parseInt(filters.page) + n;
        navigate({
            pathname: "/search",
            search: createSearchParams(filters).toString(),
        });
        window.scrollTo(0, 0);
    }

    return (
        <div className="searchPage">
            <div className="mainPage">
                <Header/>
                <SearchNav/>
                <SearchListings/>
                {paginationButtons}
            </div>
            <RightNav/>
        </div>
    )
}

export default Search;
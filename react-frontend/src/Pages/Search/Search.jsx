<<<<<<< HEAD
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
                    <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon" />&ensp;Previous</Button>
                    <Button style={{ marginLeft: "25px" }} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos className="icon" /></Button>
                </div>
            );
        }
        else {
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
=======
import SearchBar from "@/Components/SearchBar/SearchBar";
import LeftNavigation from "@/Components/LeftNavigation/LeftNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import Listings from "@/Components/Listings/Listings";
import { MdOutlineSort } from "react-icons/md";
import { Button } from "@mui/material";
import "./Search.scss";

const Search = () => {

    function toggleHomeNav(e) {
        document.querySelectorAll(".navBtn").forEach(element => {
            element.classList.remove("selected")
        });
        e.target.classList.add("selected");
>>>>>>> 7ffa840 (WIP on main)
    }

    return (
        <div className="searchPage">
<<<<<<< HEAD
            <div className="mainPage">
                <Header />
                <SearchNavigation />
                <SearchListings />
                {paginationButtons}
=======
            <div style={{height: "100%", display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "70%"}}>
                    <SearchBar />
                    <div className="headNav">
                        <Button className="navBtn selected" onClick={(e) => {toggleHomeNav(e)}}>
                            Best Results
                        </Button>
                        <Button className="navBtn" onClick={(e) => {toggleHomeNav(e)}}>
                            Best Deals
                        </Button>
                        <Button className="navBtn" onClick={(e) => {toggleHomeNav(e)}}>
                            View All
                        </Button>
                        <Button className="navBtn sortBtn">
                            Sort By&ensp; <MdOutlineSort style={{fontSize: "16px"}} />
                        </Button>
                    </div>
                    <div className="mainPage">
                        <Listings />
                    </div>
                </div>
                <RightNavigation />
>>>>>>> 7ffa840 (WIP on main)
            </div>
            <RightNavigation />
        </div>
    )
}

export default Search;
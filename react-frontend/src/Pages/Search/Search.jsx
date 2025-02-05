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
    }

    return (
        <div className="searchPage">
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
            </div>
        </div>
    )
}

export default Search;
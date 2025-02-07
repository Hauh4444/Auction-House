// External Libraries
import {createSearchParams, useNavigate} from "react-router-dom";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";
// Internal Modules
import SearchBar from "@/Components/SearchBar/SearchBar";
import CategoriesPopup from "@/Components/CategoriesPopup/CategoriesPopup";
// Stylesheets
import "./Header.scss";

const Header = () => {
    const navigate = useNavigate();

    function toggleCategoriesDisplay() {
        const element = document.querySelector(".categoriesPopup");
        element.style.maxHeight = element.style.maxHeight === "0px" || element.style.maxHeight === "" ? "100%" : "0";
    }

    return (
        <>
            <div className="header">
                <div className="headNav">
                    <Button className="navBtn" onClick={() => {
                        navigate({
                            pathname: "/",
                            search: createSearchParams({
                                nav: "home",
                            }).toString(),
                        })
                    }}>
                        Home
                    </Button>
                    <Button className="navBtn" onClick={() => {navigate("/search")}}>
                        Shop All
                    </Button>
                    <Button className="navBtn" onClick={() => {navigate("/about")}}>
                        About
                    </Button>
                    <Button className="navBtn" onClick={() => {navigate("/contact")}}>
                        Contact
                    </Button>
                    <Button className="navBtn categoriesBtn" onClick={toggleCategoriesDisplay}>
                        Categories&ensp;<BsGrid3X3GapFill className="icon" />
                    </Button>
                </div>
                <SearchBar />
            </div>
            <CategoriesPopup />
        </>
    )
}

export default Header;
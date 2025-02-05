<<<<<<< HEAD
// External Libraries
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";
// Internal Modules
import SearchBar from "@/Components/SearchBar/SearchBar";
import CategoriesNavigation from "@/Components/CategoriesNavigation/CategoriesNavigation.jsx";
// Stylesheets
import "./Header.scss";

const Header = () => {
    const navigate = useNavigate();
    const location = useLocation();

    function toggleCategoriesDisplay() {
        const element = document.querySelector(".categoriesPopup");
        element.style.maxHeight = element.style.maxHeight === "0px" || element.style.maxHeight === "" ? "100%" : "0";
    }

    return (
        <>
            <div className="header">
                <div className="headNav">
                    <Button className="btn" onClick={() => {
                        navigate({
                            pathname: "/",
                            search: createSearchParams({
                                nav: "home",
                            }).toString(),
                        })
                    }}>
                        Home
                    </Button>
                    <Button className="btn" onClick={() => {navigate("/search")}}>
                        Shop All
                    </Button>
                    <Button className="btn" onClick={() => {navigate("/about")}}>
                        About
                    </Button>
                    <Button className="btn" onClick={() => {navigate("/contact")}}>
                        Contact
                    </Button>
                    {location.pathname !== "/" ? (
                        <Button className="btn categoriesBtn" onClick={toggleCategoriesDisplay}>
                            Categories&ensp;<BsGrid3X3GapFill className="icon" />
                        </Button>
                    ) : (
                        <></>
                    )}
                </div>
                <SearchBar />
            </div>
            {location.pathname !== "/" ? (
                <CategoriesNavigation />
            ) : (
                <></>
            )}
        </>
=======
import SearchBar from "@/Components/SearchBar/SearchBar";
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import "./Header.scss"

const Header = () => {
    const navigate = useNavigate();

    return (
        <div className="header">
            <div className="headNav">
                <Button className="navBtn" onClick={() => {navigate("/")}}>
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
            </div>
            <SearchBar />
        </div>
>>>>>>> 9d377c2 (update)
    )
}

export default Header;
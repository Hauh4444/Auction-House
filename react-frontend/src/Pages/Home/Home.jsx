<<<<<<< HEAD
// External Libraries
import { useLocation } from "react-router-dom";
// Internal Modules
import CategoriesNavigation from "@/Components/CategoriesNavigation/CategoriesNavigation.jsx";
import Header from "@/Components/Header/Header";
import HomeNavigation from "@/Components/HomeNavigation/HomeNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
// Stylesheets
import "./Home.scss";

const Home = () => {
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());
=======
import SearchBar from "@//Components/SearchBar/SearchBar";
import LeftNavigation from "@//Components/LeftNavigation/LeftNavigation";
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
import CategoriesPopup from "@//Components/CategoriesPopup/CategoriesPopup";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";
import "./Home.scss"

const Home = () => {

    function toggleCategoriesDisplay() {
        let element = document.querySelector(".categoriesPopup");
        if (["0px", ""].includes(element.style.maxHeight)) {
            element.style.maxHeight = "100%";
        }
        else {
            element.style.maxHeight = "0";
        }
    }
>>>>>>> 7ffa840 (WIP on main)

    function toggleHomeNav(e) {
        document.querySelectorAll(".navBtn").forEach(element => {
            element.classList.remove("selected")
        });
        e.target.classList.add("selected");
    }

    return (
        <div className="homePage">
<<<<<<< HEAD
            <div className="mainPage">
                <Header />
                <HomeNavigation />
                {filters.nav === "home" ? (
                    <CategoriesNavigation />
                ) : (
                    <></>
                )}
=======
            <div style={{height: "100%", display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "70%"}}>
                    <SearchBar />
                    <div className="headNav">
                        <Button className="navBtn selected" onClick={(e) => {toggleHomeNav(e)}}>
                            Home
                        </Button>
                        <Button className="navBtn" onClick={(e) => {toggleHomeNav(e)}}>
                            My Orders
                        </Button>
                        <Button className="navBtn" onClick={(e) => {toggleHomeNav(e)}}>
                            My Lists
                        </Button>
                        <Button className="navBtn" onClick={(e) => {toggleHomeNav(e)}}>
                            Deals
                        </Button>
                        <Button className="navBtn" onClick={(e) => {toggleHomeNav(e)}}>
                            Sell
                        </Button>
                        <Button className="navBtn categoriesBtn" onClick={toggleCategoriesDisplay}>
                            Categories&ensp;<BsGrid3X3GapFill style={{fontSize: "16px"}} />
                        </Button>
                    </div>
                    <CategoriesPopup />
                    <div className="mainPage">
                        <div className="recommended">
                            <div className="nav">
                                <p className="head">Recommended for You</p>
                                <Button className="viewAll">
                                    View All
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
                <RightNavigation />
>>>>>>> 7ffa840 (WIP on main)
            </div>
            <RightNavigation />
        </div>
    )
};

export default Home;
import CategoriesPopup from "@/Components/CategoriesPopup/CategoriesPopup";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";
import { toggleNav } from "@/Components/Navigation/Navigation"
import "@/Components/Navigation/Navigation.scss"

const HomeNavigation = () => {

    function toggleCategoriesDisplay() {
        let element = document.querySelector(".categoriesPopup");
        if (["0px", ""].includes(element.style.maxHeight)) {
            element.style.maxHeight = "100%";
        }
        else {
            element.style.maxHeight = "0";
        }
    }

    return (
        <>
            <div className="homeNav">
                <Button className="navBtn selected" onClick={(e) => {toggleNav(e)}}>
                    Home
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    My Orders
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    My Lists
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    Deals
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    Sell
                </Button>
                <Button className="navBtn categoriesBtn" onClick={toggleCategoriesDisplay}>
                    Categories&ensp;<BsGrid3X3GapFill className="icon" />
                </Button>
            </div>
            <CategoriesPopup />
        </>
    )
}

export default HomeNavigation;
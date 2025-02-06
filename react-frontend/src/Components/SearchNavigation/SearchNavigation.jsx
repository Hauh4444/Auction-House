import { MdOutlineSort } from "react-icons/md";
import { Button } from "@mui/material";
import { toggleNav } from "@/Components/Navigation/Navigation.jsx"
import "@/Components/Navigation/Navigation.scss"

const SearchNavigation = () => {

    return (
        <>
            <div className="searchNav">
                <Button className="navBtn selected" onClick={(e) => {toggleNav(e)}}>
                    Best Results
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    Best Deals
                </Button>
                <Button className="navBtn" onClick={(e) => {toggleNav(e)}}>
                    View All
                </Button>
                <Button className="navBtn sortBtn">
                    Sort By&ensp; <MdOutlineSort className="icon" />
                </Button>
            </div>
        </>
    )
}

export default SearchNavigation;
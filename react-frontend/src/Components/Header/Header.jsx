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
    )
}

export default Header;
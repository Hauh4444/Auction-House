// External Libraries
import {useLocation, useNavigate} from "react-router-dom";
import {BsGrid3X3GapFill} from "react-icons/bs";
import {Button} from "@mui/material";
// Internal Modules
import Bar from "@/Components/Search/Bar/Bar";
import CategoryNav from "@/Components/Navigation/Category/CategoryNav.jsx";
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
                        navigate("/")
                    }}>

                        Home
                    </Button>
                    <Button className="btn" onClick={() => {
                        navigate("/search")
                    }}>
                        Shop All
                    </Button>
                    <Button className="btn" onClick={() => {
                        navigate("/about")
                    }}>
                        About
                    </Button>
                    <Button className="btn" onClick={() => {
                        navigate("/contact")
                    }}>
                        Contact
                    </Button>
                    {location.pathname !== "/" ? (
                        <Button className="btn categoriesBtn" onClick={toggleCategoriesDisplay}>
                            Categories&ensp;<BsGrid3X3GapFill className="icon"/>
                        </Button>
                    ) : (
                        <></>
                    )}
                </div>
                <Bar/>
            </div>
            {location.pathname !== "/" ? (
                <CategoryNav/>
            ) : (
                <></>
            )}
        </>
    )
}

export default Header;
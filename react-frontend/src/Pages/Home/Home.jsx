import SearchBar from "../../Components/SearchBar/SearchBar";
import LeftNavigation from "../../Components/LeftNavigation/LeftNavigation.jsx";
import RightNavigation from "../../Components/RightNavigation/RightNavigation.jsx";
import CategoryNavigation from "../../Components/CategoryNavigation/CategoryNavigation.jsx";
import { BsGrid3X3GapFill } from "react-icons/bs";
import { Button } from "@mui/material";
import './Home.scss'

const Home = () => {

    function toggleCategoriesDisplay() {
        let element = document.querySelector(".categoryNav");
        console.log(element.style.maxHeight);
        if (["0px", ""].includes(element.style.maxHeight)) {
            element.style.maxHeight = "100vh";
        }
        else {
            element.style.maxHeight = "0";
        }
    }

    return (
        <div className="homePage">
            <div style={{display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "50%"}}>
                    <SearchBar />
                    <div className="mainPage">
                        <div className="homeNav">
                            <Button className="navBtn selected">
                                Home
                            </Button>
                            <Button className="navBtn">
                                My Orders
                            </Button>
                            <Button className="navBtn">
                                My Lists
                            </Button>
                            <Button className="navBtn">
                                Deals
                            </Button>
                            <Button className="navBtn">
                                Sell
                            </Button>
                            <Button className="navBtn categoriesBtn" onClick={toggleCategoriesDisplay}>
                                Categories&ensp;<BsGrid3X3GapFill style={{fontSize: "16px"}} />
                            </Button>
                        </div>
                        <CategoryNavigation />
                        <div className="featured">

                        </div>
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
            </div>
        </div>
    )
};

export default Home;
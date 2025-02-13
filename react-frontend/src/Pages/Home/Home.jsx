// External Libraries
import {useLocation} from "react-router-dom";
// Internal Modules
import CategoryNav from "@/Components/Navigation/Category/CategoryNav.jsx";
import Header from "@/Components/Header/Header";
import HomeNav from "@/Components/Navigation/Home/HomeNav.jsx";
import RightNav from "@/Components/Navigation/Right/RightNav.jsx";
// Stylesheets
import "./Home.scss";

const Home = () => {
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    return (
        <div className="homePage">
            <div className="mainPage">
                <Header/>
                <HomeNav/>
                {!filters.nav ? (
                    <CategoryNav/>
                ) : (
                    <></>
                )}
            </div>
            <RightNav/>
        </div>
    )
};

export default Home;
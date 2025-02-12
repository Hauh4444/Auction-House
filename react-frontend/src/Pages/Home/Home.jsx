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

    return (
        <div className="homePage">
            <div className="mainPage">
                <Header />
                <HomeNavigation />
                {filters.nav === "home" ? (
                    <CategoriesNavigation />
                ) : (
                    <></>
                )}
            </div>
            <RightNavigation />
        </div>
    )
};

export default Home;
// External Libraries
import { useLocation } from "react-router-dom";
// Internal Modules
import CategoryNav from "@/Components/Navigation/CategoryNav/CategoryNav";
import Header from "@/Components/Header/Header";
import HomeNav from "@/Components/Navigation/HomeNav/HomeNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
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
                {!filters.nav && (
                    <CategoryNav/>
                )}
            </div>
            <RightNav/>
        </div>
    )
};

export default Home;
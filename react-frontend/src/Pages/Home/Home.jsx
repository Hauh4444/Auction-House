// External Libraries
import { Button } from "@mui/material";
// Internal Modules
import Header from "@/Components/Header/Header";
import HomeNavigation from "@/Components/HomeNavigation/HomeNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
// Stylesheets
import "./Home.scss";


const Home = () => {

    return (
        <div className="homePage">
            <div className="mainPage">
                <Header />
                <HomeNavigation />
                <div className="content">
                    <div className="recommended">
                        <div className="nav">
                            <p className="head">Recommended for You</p>
                            <Button className="viewAll">View All</Button>
                        </div>
                    </div>
                </div>
            </div>
            <RightNavigation />
        </div>
    )
};

export default Home;
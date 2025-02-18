// External Libraries
import { useLocation } from "react-router-dom";

// Internal Modules
import CategoryNav from "@/Components/Navigation/CategoryNav/CategoryNav";
import Header from "@/Components/Header/Header";
import HomeNav from "@/Components/Navigation/HomeNav/HomeNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./Home.scss";

/**
 * Home Component
 *
 * This component represents the homepage of the application.
 * It dynamically adjusts content based on URL query parameters.
 *
 * Features:
 * - Displays a header and main navigation.
 * - Optionally renders the `CategoryNav` component if 'nav' filter is not present.
 * - Includes a right-side navigation panel.
 */
const Home = () => {
    const location = useLocation(); // Hook to access the current location (URL)
    // Extract query parameters from the URL
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    return (
        <div className="homePage">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                {/* Home Navigation */}
                <HomeNav />
                {/* Category Navigation - displayed if 'Home' navigation is toggled */}
                {!filters.nav && (
                    <CategoryNav />
                )}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default Home;

// Internal Modules
import CategoryNav from "@/Components/Navigation/CategoryNav/CategoryNav";
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

/**
 * Home Component
 *
 * This component represents the homepage of the application. It dynamically adjusts its content
 * based on URL query parameters, providing a tailored user experience.
 *
 * Features:
 * - Displays a header and main navigation for the application.
 * - Renders the "CategoryNav" Component.
 * - Includes a right-side navigation panel for additional navigation options.
 *
 * @returns {JSX.Element} The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
 */
const Home = () => {

    return (
        <div className="homePage page" data-testid="homePage">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                {/* Category Navigation */}
                <CategoryNav />
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default Home;

// External Libraries
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import image from "@/assets/images/404.jpg";

// Stylesheets
import "./PageNotFound.scss"

/**
 * PageNotFound Component
 *
 * This component renders a 404 error page when a user navigates to a non-existent route.
 *
 * Features:
 * - Displays a "Page Not Found" image.
 * - Provides a link to navigate back to the home page.
 *
 * @returns { JSX.Element } The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
 */
const PageNotFound = () => {
    const navigate = useNavigate();

    return (
        <div className="pageNotFoundPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <div className="content">
                    <div className="notFound">
                        <div className="image">
                            <img src={ image } alt="Page Not Found" />
                        </div>
                        <Button className="btn" onClick={ () => navigate("/") }>
                            Back to Home
                        </Button>
                    </div>
                </div>
            </div>
            <RightNav />
        </div>
    )
}

export default PageNotFound;

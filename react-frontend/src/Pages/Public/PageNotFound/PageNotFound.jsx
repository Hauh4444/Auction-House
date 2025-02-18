// External Libraries
import { Link } from "react-router-dom";

// Stylesheets
import "./PageNotFound.scss";

/**
 * PageNotFound Component
 *
 * This component renders a 404 error page when a user navigates to a non-existent route.
 *
 * Features:
 * - Displays a 'Page Not Found' image.
 * - Provides a link to navigate back to the home page.
 */
const PageNotFound = () => {
    return (
        <>
            <section className="mainSection">
                <img src="/assets/404.jpg" className="notFoundImage" alt="Page Not Found" />
            </section>
            <div>
                <Link to="/">
                    Back to Home
                </Link>
            </div>
        < />
    )
}

export default PageNotFound;

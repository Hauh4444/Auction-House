// External Libraries
import { Link } from "react-router-dom";

/**
 * PageNotFound Component
 *
 * This component renders a 404 error page when a user navigates to a non-existent route.
 *
 * Features:
 * - Displays a "Page Not Found" image.
 * - Provides a link to navigate back to the home page.
 *
 * @returns {JSX.Element} The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
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

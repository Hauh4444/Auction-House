<<<<<<< HEAD
// External Libraries
import { Link } from "react-router-dom";
// Stylesheets
=======
import { Link } from "react-router-dom";
>>>>>>> 7ffa840 (WIP on main)
import "./PageNotFound.scss";

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
        </>
    )
}

export default PageNotFound;
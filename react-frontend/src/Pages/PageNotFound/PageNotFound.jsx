import { Link } from "react-router-dom";
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
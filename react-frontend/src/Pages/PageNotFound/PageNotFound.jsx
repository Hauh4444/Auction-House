import { Link } from 'react-router-dom';
import Header from '../../Components/Header/Header';
import './PageNotFound.scss';

const PageNotFound = () => {
    return (
        <>
            <Header />
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
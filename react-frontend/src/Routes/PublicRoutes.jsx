import { Routes, Route } from 'react-router-dom';
import Home from "../Pages/Home/Home";
import Category from "../Pages/Category/Category";
import Search from "../Pages/Search/Search";
import Listing from "../Pages/Listing/Listing.jsx";
import SignIn from "../Pages/SignIn/SignIn";
import CreateAccount from "../Pages/CreateAccount/CreateAccount";
import PageNotFound from "../Pages/PageNotFound/PageNotFound";

const PublicRoutes = () => {
    return (
        <>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/categories" element={<Category />} />
                <Route path="/search" element={<Search />} />
                <Route path="/listings" element={<Listing />} />
                <Route path="/sign-in" element={<SignIn />} />
                <Route path="/create-account" element={<CreateAccount />} />
                <Route path="*" element={<PageNotFound />} />
            </Routes>
        </>
    )
};

export default PublicRoutes;
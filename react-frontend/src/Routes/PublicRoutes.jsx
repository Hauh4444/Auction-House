import { Routes, Route } from "react-router-dom";
import Home from "@/Pages/Home/Home";
import Search from "@/Pages/Search/Search";
import Category from "@/Pages/Category/Category";
import Listing from "@/Pages/Listing/Listing";
import SignIn from "@/Pages/SignIn/SignIn";
import CreateAccount from "@/Pages/CreateAccount/CreateAccount";
import About from "@/Pages/About/About";
import Contact from "@/Pages/Contact/Contact";
import PageNotFound from "@/Pages/PageNotFound/PageNotFound";

const PublicRoutes = () => {
    return (
        <>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/search" element={<Search />} />
                <Route path="/category" element={<Category />} />
                <Route path="/listings" element={<Listing />} />
                <Route path="/sign-in" element={<SignIn />} />
                <Route path="/create-account" element={<CreateAccount />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="*" element={<PageNotFound />} />
            </Routes>
        </>
    )
};

export default PublicRoutes;
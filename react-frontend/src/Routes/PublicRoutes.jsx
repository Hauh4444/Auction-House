<<<<<<< HEAD
// External Libraries
import { Routes, Route } from "react-router-dom";
// Internal Modules
=======
import { Routes, Route } from "react-router-dom";
>>>>>>> 7ffa840 (WIP on main)
import Home from "@/Pages/Home/Home";
import Search from "@/Pages/Search/Search";
import Category from "@/Pages/Category/Category";
import Listing from "@/Pages/Listing/Listing";
import SignIn from "@/Pages/SignIn/SignIn";
import CreateAccount from "@/Pages/CreateAccount/CreateAccount";
<<<<<<< HEAD
<<<<<<< HEAD
import About from "@/Pages/About/About";
import Contact from "@/Pages/Contact/Contact";
=======
>>>>>>> 7ffa840 (WIP on main)
=======
import About from "@/Pages/About/About";
import Contact from "@/Pages/Contact/Contact";
>>>>>>> 9d377c2 (update)
import PageNotFound from "@/Pages/PageNotFound/PageNotFound";

const PublicRoutes = () => {
    return (
<<<<<<< HEAD
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
=======
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
>>>>>>> 7ffa840 (WIP on main)
    )
};

export default PublicRoutes;
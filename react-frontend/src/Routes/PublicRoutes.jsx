// External Libraries
import { Route, Routes } from "react-router-dom";
// Internal Modules
import AuthProvider from "@/ContextAPI/AuthProvider"
import Home from "@/Pages/Home/Home";
import Search from "@/Pages/Search/Search";
import Category from "@/Pages/Category/Category";
import Listing from "@/Pages/Listing/Listing";
import AuthPage from "@/Pages/AuthPage/AuthPage";
import About from "@/Pages/About/About";
import Contact from "@/Pages/Contact/Contact";
import PageNotFound from "@/Pages/PageNotFound/PageNotFound";
// Private Internal Modules
import PrivateRoute from "@/Routes/PrivateRoute"
import Account from "@/Pages/Account/Account"

const PublicRoutes = () => {

    return (
        <AuthProvider>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/search" element={<Search/>}/>
                <Route path="/category" element={<Category/>}/>
                <Route path="/listing" element={<Listing/>}/>
                <Route path="/auth-page" element={<AuthPage/>}/>
                <Route path="/about" element={<About/>}/>
                <Route path="/contact" element={<Contact/>}/>
                <Route path="*" element={<PageNotFound/>}/>

                <Route element={<PrivateRoute />}>
                    <Route path="/account" element={<Account />} />
                </Route>
            </Routes>
        </AuthProvider>
    )
};

export default PublicRoutes;
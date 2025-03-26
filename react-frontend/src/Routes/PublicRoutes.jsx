// External Libraries
import { Route, Routes } from "react-router-dom";

// Public Internal Modules
import About from "@/Pages/Public/About/About";
import AuthPage from "@/Pages/Public/AuthPage/AuthPage";
import Browse from "@/Pages/Public/Browse/Browse";
import Category from "@/Pages/Public/Category/Category";
import Contact from "@/Pages/Public/Contact/Contact";
import Home from "@/Pages/Public/Home/Home";
import Listing from "@/Pages/Public/Listing/Listing";
import PageNotFound from "@/Pages/Public/PageNotFound/PageNotFound";
import Search from "@/Pages/Public/Search/Search";
import Support from "@/Pages/Public/Support/Support";

// Internal Authentication Modules
import AuthProvider from "@/ContextAPI/AuthProvider";
import PrivateRoute from "@/Routes/PrivateRoute";
import StaffRoute from "@/Routes/StaffRoute";
import AdminRoute from "@/Routes/AdminRoute";

// Private Internal Modules
import Cart from "@/Pages/Private/Cart/Cart";
import Deliveries from "@/Pages/Private/Deliveries/Deliveries";
import History from "@/Pages/Private/History/History";
import Lists from "@/Pages/Private/Lists/Lists";
import ManageListing from "@/Pages/Private/ManageListing/ManageListing";
import Messages from "@/Pages/Private/Messages/Messages";
import MyBids from "@/Pages/Private/MyBids/MyBids";
import PaymentInfo from "@/Pages/Private/PaymentInfo/PaymentInfo";
import Report from "@/Pages/Private/Report/Report";
import Review from "@/Pages/Private/Review/Review";
import Security from "@/Pages/Private/Security/Security";
import SellerProfile from "@/Pages/Private/SellerProfile/SellerProfile";
import UserAccount from "@/Pages/Private/UserAccount/UserAccount";
import UserProfile from "@/Pages/Private/UserProfile/UserProfile";

// Staff Internal Modules
import CustomerInquiries from "@/Pages/Staff/CustomerInquiries/CustomerInquiries";
import ListingReports from "@/Pages/Staff/ListingReports/ListingReports";
import ManageListings from "@/Pages/Staff/ManageListings/ManageListings";
import StaffAccount from "@/Pages/Staff/StaffAccount/StaffAccount";
import StaffDashboard from "@/Pages/Staff/StaffDashboard/StaffDashboard";
import StaffProfile from "@/Pages/Staff/StaffProfile/StaffProfile";

// Admin Internal Modules
import AdminAccount from "@/Pages/Admin/AdminAccount/AdminAccount";
import AdminDashboard from "@/Pages/Admin/AdminDashboard/AdminDashboard";
import AdminProfile from "@/Pages/Admin/AdminProfile/AdminProfile";
import ManageUsers from "@/Pages/Admin/ManageUsers/ManageUsers";
import SiteSettings from "@/Pages/Admin/SiteSettings/SiteSettings";
import SystemLogs from "@/Pages/Admin/SystemLogs/SystemLogs";

/**
 * PublicRoutes Component
 *
 * This component defines the routing structure for both public and private sections of the application.
 * It utilizes the `AuthProvider` context to manage the user"s authentication state. The routing setup includes:
 * - Public routes that are accessible to all users.
 * - Private routes that are protected by the `PrivateRoute` component, allowing access only to authenticated users.
 * - Staff routes that are protected by the `StaffRoute` component, allowing access only to authenticated users with staff privileges.
 * - Admin routes that are protected by the `AdminRoute` component, allowing access only to authenticated users with admin privileges.
 *
 * @returns {JSX.Element} The configured routes for public and private pages.
 */
const PublicRoutes = () => {

    return (
        <AuthProvider>
            <Routes>
                {/* Public Routes */}
                <Route path="/about" element={<About />} />
                <Route path="/auth-page" element={<AuthPage />} />
                <Route path="/browse" element={<Browse />} />
                <Route path="/category" element={<Category />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/" element={<Home />} />
                <Route path="/listing" element={<Listing />} />
                <Route path="*" element={<PageNotFound />} />
                <Route path="/search" element={<Search />} />
                <Route path="/support" element={<Support />} />

                {/* Protected Routes for Authenticated Users */}
                <Route element={<PrivateRoute />}>
                    <Route path="/user/cart" element={<Cart />} />
                    <Route path="/user/deliveries" element={<Deliveries />} />
                    <Route path="/user/history" element={<History />} />
                    <Route path="/user/lists" element={<Lists />} />
                    <Route path="/user/listings/:id" element={<ManageListing />} />
                    <Route path="/user/messages" element={<Messages />} />
                    <Route path="/user/my-bids" element={<MyBids />} />
                    <Route path="/user/payment-info" element={<PaymentInfo />} />
                    <Route path="/user/report" element={<Report />} />
                    <Route path="/user/review" element={<Review />} />
                    <Route path="/user/security" element={<Security />} />
                    <Route path="/user/seller-profile" element={<SellerProfile />} />
                    <Route path="/user/account" element={<UserAccount />} />
                    <Route path="/user/profile" element={<UserProfile />} />
                </Route>

                {/* Protected Routes for Staff Users */}
                <Route element={<StaffRoute />}>
                    <Route path="/staff/messages" element={<CustomerInquiries />} />
                    <Route path="/staff/reports" element={<ListingReports />} />
                    <Route path="/staff/manage-listings" element={<ManageListings />} />
                    <Route path="/staff/account" element={<StaffAccount />} />
                    <Route path="/staff/dashboard" element={<StaffDashboard />} />
                    <Route path="/staff/profile" element={<StaffProfile />} />
                </Route>

                {/* Protected Routes for Admin Users */}
                <Route element={<AdminRoute />}>
                    <Route path="/admin/account" element={<AdminAccount />} />
                    <Route path="/admin/dashboard" element={<AdminDashboard />} />
                    <Route path="/admin/profile" element={<AdminProfile />} />
                    <Route path="/admin/users" element={<ManageUsers />} />
                    <Route path="/admin/settings" element={<SiteSettings />} />
                    <Route path="/admin/logs" element={<SystemLogs />} />
                </Route>
            </Routes>
        </AuthProvider>
    )
};

export default PublicRoutes;

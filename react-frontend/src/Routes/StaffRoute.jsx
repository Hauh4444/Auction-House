// External Libraries
import { Navigate, Outlet } from "react-router-dom";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

/**
 * StaffRoute Component
 *
 * This component is used to protect routes that require staff privelages.
 * If the user is not authenticated, it redirects them to the login page.
 * If the user is authenticated without staff privelages, it redirects them to the home page.
 * If the user is authenticated, it renders the child routes by using the Outlet component.
 *
 * @returns {JSX.Element}
 */
const StaffRoute = () => {
    // Fetch the authentication context
    const auth = useAuth();

    // If the user is not authenticated, redirect to the authentication page
    if (!auth.user) return <Navigate to="/auth-page" />;

    // If user does not have staff privelages, redirect to the home page
    if (auth.user.role !== "staff") return <Navigate to="/" />

    // If the user is authenticated with staff privelages, render the child routes
    return <Outlet />;
};

export default StaffRoute;

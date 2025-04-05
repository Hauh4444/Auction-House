// External Libraries
import { Navigate, Outlet, useLocation } from "react-router-dom";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthContext";

/**
 * AdminRoute Component
 *
 * This component protects routes that require staff privileges. It checks the user's authentication
 * status and role, redirecting users as necessary:
 * - If the user is not authenticated, they are redirected to the login page.
 * - If the user is authenticated but does not have staff privileges, they are redirected to the home page.
 * - If the user is authenticated with staff privileges, the child routes are rendered using the Outlet component.
 *
 * @returns {JSX.Element} The rendered output, which could be a redirection or the child routes.
 */
const StaffRoute = () => {
    // Fetch the authentication context
    const auth = useAuth();
    const location = useLocation(); // Get current attempted location

    // If the user is not authenticated, redirect to the authentication page
    if (!auth.user) return <Navigate to="/auth-page" state={{ from: location }} />;

    // If user does not have staff privelages, redirect to the home page
    if (auth.user.role !== "staff") return <Navigate to="/" />

    // If the user is authenticated with staff privelages, render the child routes
    return <Outlet />;
};

export default StaffRoute;

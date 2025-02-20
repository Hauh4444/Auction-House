// External Libraries
import { Navigate, Outlet } from "react-router-dom";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

/**
 * StaffRoute Component
 *
 * This component is designed to protect routes that require staff privileges.
 * It ensures that only authenticated users with the appropriate role can access specific sections of the application.
 *
 * Features:
 * - Redirects unauthenticated users to the login page.
 * - Redirects authenticated users without staff privileges to the home page.
 * - Renders child routes for authenticated staff users using the Outlet component.
 *
 * @returns {JSX.Element}
 * - Redirects to the authentication page if the user is not logged in.
 * - Redirects to the home page if the user lacks staff privileges.
 * - Renders the child routes if the user is authenticated with staff privileges.
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

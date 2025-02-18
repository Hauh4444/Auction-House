// External Libraries
import { Navigate, Outlet } from "react-router-dom";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

/**
 * PrivateRoute Component
 *
 * This component is used to protect routes that require authentication.
 * If the user is not authenticated, it redirects them to the login page.
 * If the user is authenticated, it renders the child routes by using the Outlet component.
 *
 * @returns {JSX.Element} A Redirect to the login page or allow the protected routes.
 */
const PrivateRoute = () => {
    // Fetch the authentication context
    const auth = useAuth();

    // If the user is not authenticated, redirect to the authentication page
    if (!auth.user) return <Navigate to="/auth-page" />;

    // If the user is authenticated, render the child routes
    return <Outlet />;
};

export default PrivateRoute;

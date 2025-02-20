// External Libraries
import { Navigate, Outlet } from "react-router-dom";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

/**
 * PrivateRoute Component
 *
 * This component is used to protect routes that require user authentication. It ensures that:
 * - If the user is not authenticated, they are redirected to the login page.
 * - If the user is authenticated, the component renders the child routes using the Outlet component.
 *
 * @returns {JSX.Element} A redirection to the login page or the child protected routes.
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

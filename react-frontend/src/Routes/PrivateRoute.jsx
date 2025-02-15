// External Libraries
import { Navigate, Outlet } from "react-router-dom";
// Internal Modules
import { useAuth } from "@/ContextAPI/AuthProvider";

const PrivateRoute = () => {
    const auth = useAuth();
    if (!auth.user) return <Navigate to="/auth-page" />;
    return <Outlet />;
};

export default PrivateRoute;
// Internal Modules
import AuthForm from "@/Components/Auth/AuthForm/AuthForm";

/**
 * AuthPage Component
 *
 * This component renders the authentication page, providing a centralized UI for user login
 * and registration. It primarily consists of an `AuthForm` component, which handles user
 * authentication input and submission.
 *
 * Features:
 * - Displays the `AuthForm` component for user authentication.
 * - Provides a structured layout for login and registration.
 *
 * @returns {JSX.Element} The rendered authentication page component.
 */
const AuthPage = () => {

    return (
        <div className="authPage page">
            <AuthForm />
        </div>
    )
};

export default AuthPage;

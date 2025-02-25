// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import UserProfileCard from "@/Components/User/UserProfileCard/UserProfileCard";

/**
 * UserProfile Component
 *
 * This component renders the user profile page, including a header, a user profile card,
 * and a right-side navigation panel. It provides a structured layout where the main content
 * is displayed in the center, and additional navigation options are available on the right.
 *
 * Features:
 * - Displays a persistent header (`Header`).
 * - Shows the user's profile details using `UserProfileCard`.
 * - Includes a right-side navigation menu (`RightNav`) for additional options.
 *
 * @returns {JSX.Element} The rendered UserProfile page component.
 */
const UserProfile = () => {
    return (
        <div className="userProfilePage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                {/* User Profile Card */}
                <UserProfileCard />
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default UserProfile;
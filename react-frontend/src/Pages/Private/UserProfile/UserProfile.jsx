// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import UserProfileCard from "@/Components/User/UserProfileCard/UserProfileCard";

// Stylesheets
import "./UserProfile.scss";

const UserProfile = () => {
    return (
        <div className="userProfilePage">
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
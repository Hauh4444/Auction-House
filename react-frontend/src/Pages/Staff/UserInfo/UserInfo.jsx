// External Libraries
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./UserInfo.scss";

const UserInfo = () => {
    return (
        <div className="userInfoPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <h1>User Info</h1>
                
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default UserInfo;
// External Libraries
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./StaffAccount.scss";

const StaffAccount = () => {
    const navigate = useNavigate(); // Navigate hook for routing

    const cardInfo = {
        "messages": "Customer Inquiries",
        "manage-listings": "Manage Listings",
        "profile": "Profile",
        "reports": "Reports",
    };

    return (
        <div className="staffAccountPage page" data-testid="staffAccountPage">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <h1>Your Account</h1>
                {/* Account Navigation Cards */}
                <div className="accountNav">
                    {/* Map Dictionary to Cards */}
                    {Object.keys(cardInfo).map((key, index) => (
                        <Button
                            className={"navBtn"}
                            onClick={() => {navigate("/staff/" + key)}}
                            key={index}
                        >
                            <h2>{cardInfo[key]}</h2>
                        </Button>
                    ))}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default StaffAccount;
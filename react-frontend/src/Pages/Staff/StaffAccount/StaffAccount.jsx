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
        "/staff/messages": ["Customer Inquiries", "View and respond to customer messages and inquiries."],
        "/staff/profile": ["Profile", "Update personal details, preferences, and account settings."],
        "/staff/manage-listings": ["Manage Listings", "Manage product listings and auctions."],
        "/staff/user-info": ["Manage Users", "View, create, edit, and manage user information."],
        "/staff/reports": ["Reports", "View sales, performance, and analytical reports."]
    };

    return (
        <div className="staffAccountPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <h1>Staff Account</h1>
                { /* Account Navigation Cards */ }
                <div className="accountNav">
                    { /* Map Dictionary to Cards */ }
                    {Object.keys(cardInfo).map((key, index) => (
                        <Button
                            className={ "navBtn" }
                            onClick={ () => { navigate(key) } }
                            key={ index }
                        >
                            <h2>{ cardInfo[key][0] }</h2>
                            <p>{ cardInfo[key][1] }</p>
                        </Button>
                    ))}
                </div>
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
}

export default StaffAccount;
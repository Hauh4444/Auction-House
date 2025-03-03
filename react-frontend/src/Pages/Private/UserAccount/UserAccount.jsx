// External Libraries
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./UserAccount.scss";

/**
 * UserAccount Component
 *
 * This component renders the user account page, including a header, navigation cards,
 * and a right-side navigation panel. It provides a structured layout where the main content
 * is displayed in the center, and additional navigation options are available on the right.
 *
 * Features:
 * - Displays a persistent header (`Header`).
 * - Shows the user's account navigation.
 * - Includes a right-side navigation menu (`RightNav`) for additional options.
 *
 * @returns {JSX.Element} The rendered UserAccount page component.
 */
const UserAccount = () => {
    const navigate = useNavigate();

    const cardInfo = {
        "orders": ["Your History", "View and manage your orders"],
        "security": ["Login & Security", "Edit login information: username, password, etc"],
        "profile": ["Your Profile", "Edit profile information: name, address, etc "],
        "payment-info": ["Your Payments", "View transactions, manage payment methods and settings"],
        "lists": ["Your Lists", "View, modify, and share your lists, or create new ones"],
        "seller-profile": ["Seller Profile", "View and manage your seller profile"],
        "report": ["Customer Service", "Browse self service options or speak with a staff member"],
        "messages": ["Your Messages", "View or respond to messages from other Sellers and Buyers"]
    };

    return (
        <div className="userAccountPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
                <h1>Your Account</h1>
                {/* Account Navigation Cards */}
                <div className="accountNav">
                    {/* Map Dictionary to Cards */}
                    {Object.keys(cardInfo).map((key, index) => (
                        <Button
                            className={`navBtn ${index % 3 === 0 ? "first" : ""}`}
                            onClick={() => {navigate("/user/" + key)}}
                            key={index}
                        >
                            <h2>{cardInfo[key][0]}</h2>
                            <p>{cardInfo[key][1]}</p>
                        </Button>
                    ))}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    )
}

export default UserAccount;
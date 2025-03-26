// External Libraries
import { useNavigate } from "react-router-dom";
import { BsThreeDots } from "react-icons/bs";
import { RiAccountCircle2Fill, RiAccountCircle2Line } from "react-icons/ri";
import { IoCart, IoCartOutline, IoFlag, IoFlagOutline } from "react-icons/io5";
import { HiOutlineUserGroup, HiUserGroup } from "react-icons/hi2";
import { PiTruckFill, PiTruckLight } from "react-icons/pi";
import { Button } from "@mui/material";

// Stylesheets
import "./RightNav.scss";

// Custom Variables
import { variables } from "@/assets/variables.modules";

/**
 * RightNav Component
 *
 * This component renders a navigation sidebar that provides users with access
 * to various features of the application. It includes buttons for account
 * management, notifications, cart functionality, user groups, and shipping
 * options, each represented by relevant icons. The buttons are styled using
 * Material-UI components and positioned using flexbox to maintain a clean
 * layout.
 *
 * Features:
 * - Navigates to the account page when the account button is clicked.
 * - Includes icons for visual representation of each feature, enhancing
 *   user experience.
 *
 * @returns {JSX.Element} A sidebar navigation component with buttons
 *                       corresponding to different functionalities of the
 *                       application.
 */
const RightNav = () => {
    const navigate = useNavigate(); // Navigate hook for routing

    return (
        <nav className="rightNav"> {/* Navigation container */}
            <div className="navBar"> {/* Navigation bar container */}
                <Button className="btn" data-testid="menuBtn"> {/* Button for menu */}
                    <BsThreeDots className="menuBtn" style={{
                        fontSize: "25px", // Font size for the menu icon
                        color: variables.mainColor3, // Custom color from variables
                    }} />
                </Button>
                <Button className="btn" data-testid="accountBtn" style={{marginBottom: "15px"}} onClick={() => navigate("/user/account")}>
                    <RiAccountCircle2Fill className="fill" /> {/* Filled account icon */}
                    <RiAccountCircle2Line className="outline" /> {/* Outlined account icon */}
                </Button>
                <Button className="btn" data-testid="flagBtn" style={{marginBottom: "15px"}} onClick={() => navigate("/support")}> {/* Button for flag */}
                    <IoFlag className="fill" /> {/* Filled flag icon */}
                    <IoFlagOutline className="outline" /> {/* Outlined flag icon */}
                </Button>
                <Button className="btn" data-testid="cartBtn" style={{marginBottom: "15px"}} onClick={() => navigate("/user/cart")}>
                    <IoCart className="fill" /> {/* Filled cart icon */}
                    <IoCartOutline className="outline" /> {/* Outlined cart icon */}
                </Button>
                <Button className="btn" data-testid="friendBtn" style={{marginBottom: "15px"}} onClick={() => navigate("/user/messages")}> {/* Button for user group */}
                    <HiUserGroup className="fill" /> {/* Filled user group icon */}
                    <HiOutlineUserGroup className="outline" /> {/* Outlined user group icon */}
                </Button>
                <Button className="btn" data-testid="truckBtn" style={{marginBottom: "15px"}} onClick={() => navigate("/user/deliveries")}>
                    <PiTruckFill className="fill" /> {/* Filled truck icon */}
                    <PiTruckLight className="outline" /> {/* Outlined truck icon */}
                </Button>
            </div>
        </nav>
    )
};

export default RightNav;
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
import { variables } from "@/assets/variables.modules.js";

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
    const navigate = useNavigate();

    return (
        <nav className="rightNav" style={{flexBasis: "15%"}}>
            <div className="navBar">
                <Button className="btn">
                    <BsThreeDots className="menuBtn" style={{
                        fontSize: "25px",
                        color: variables.mainColor3,
                    }} />
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}} onClick={() => navigate("/account")}>
                    <RiAccountCircle2Fill className="fill" />
                    <RiAccountCircle2Line className="outline" />
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <IoFlag className="fill" />
                    <IoFlagOutline className="outline" />
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <IoCart className="fill" />
                    <IoCartOutline className="outline" />
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <HiUserGroup className="fill" />
                    <HiOutlineUserGroup className="outline" />
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <PiTruckFill className="fill" />
                    <PiTruckLight className="outline" />
                </Button>
            </div>
        </nav>
    )
};

export default RightNav;
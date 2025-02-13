// External Libraries
import {useNavigate} from "react-router-dom";
import {BsThreeDots} from "react-icons/bs";
import {RiAccountCircle2Fill, RiAccountCircle2Line} from "react-icons/ri";
import {IoCart, IoCartOutline, IoFlag, IoFlagOutline} from "react-icons/io5";
import {HiOutlineUserGroup, HiUserGroup} from "react-icons/hi2";
import {PiTruckFill, PiTruckLight} from "react-icons/pi";
import {Button} from "@mui/material";
// Stylesheets
import "./RightNav.scss";
// Custom Variables
import {variables} from "@/assets/variables.modules.js";

const RightNav = () => {
    const navigate = useNavigate();

    return (
        <nav className="rightNav" style={{flexBasis: "15%"}}>
            <div className="navBar">
                <Button className="btn">
                    <BsThreeDots className="menuBtn" style={{
                        fontSize: "25px",
                        color: variables.mainColor3,
                    }}/>
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <RiAccountCircle2Fill className="fill"/>
                    <RiAccountCircle2Line className="outline"/>
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <IoFlag className="fill"/>
                    <IoFlagOutline className="outline"/>
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <IoCart className="fill"/>
                    <IoCartOutline className="outline"/>
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <HiUserGroup className="fill"/>
                    <HiOutlineUserGroup className="outline"/>
                </Button>
                <Button className="btn" style={{marginBottom: "15px"}}>
                    <PiTruckFill className="fill"/>
                    <PiTruckLight className="outline"/>
                </Button>
            </div>
        </nav>
    )
};

export default RightNav;
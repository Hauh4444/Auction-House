import { useNavigate } from "react-router-dom";
import { TiHomeOutline } from "react-icons/ti";
import { Button } from "@mui/material";
import "./LeftNavigation.scss"


const LeftNavigation = () => {
    const navigate = useNavigate();

    return (
        <div className="leftNav" style={{flexBasis: "15%"}}>
            <Button className="navBtn" onClick={() => {navigate("/")}}>
                &emsp;<TiHomeOutline className="icon" />&emsp;Home
            </Button>
        </div>
    )
}

export default LeftNavigation;
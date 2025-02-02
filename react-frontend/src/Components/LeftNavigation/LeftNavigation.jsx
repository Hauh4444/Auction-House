import { useNavigate } from "react-router-dom";
import { TiHomeOutline } from "react-icons/ti";
import { Button } from "@mui/material";
import './LeftNavigation.scss'
import variables from "../../variables.module.scss";

const LeftNavigation = () => {
    const navigate = useNavigate();

    return (
        <div className="leftNav" style={{flexBasis: "25%"}}>
            <Button className="navBtn" onClick={() => {navigate('/')}}>
                &emsp;<TiHomeOutline style={{
                position: "relative",
                top: "3px",
                fontSize: "16px",
                color: variables.accentColor3
            }} />&emsp;Home
            </Button>
        </div>
    )
}

export default LeftNavigation;
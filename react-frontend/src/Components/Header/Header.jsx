import Navigation from '../Navigation/Navigation.jsx';
import SearchBar from '../SearchBar/SearchBar';
import { useNavigate } from 'react-router-dom';
import { MdCurrencyExchange, MdOutlineLocationOn } from "react-icons/md";
import { RxCornerTopLeft, RxCornerBottomLeft } from "react-icons/rx";
import { Button } from "@mui/material";
import './Header.scss';

const Header = () => {
    const navigate = useNavigate();

    function goToHome() {
        navigate('/');
    }

    function goToSignIn() {
        navigate('/sign-in');
    }

    return (
        <div className="header">
            <div style={{display: 'flex', flexDirection: 'row'}}>
                <div style={{flexBasis: "25%", height: "56px"}}>
                    <Button className="homeBtn headBtn" onClick={goToHome}>
                        Home
                    </Button>
                </div>
                <div style={{flexBasis: "50%", height: "56px"}}>
                    <SearchBar />
                </div>
                <div style={{flexBasis: "25%", height: "56px"}}>
                    <div style={{display: "flex", flexDirection: "row"}}>
                        <div style={{margin: "auto 0 auto 0", display: "flex", flexDirection: "column"}}>
                            <div className="topCornerIcon cornerIcon">
                                <RxCornerTopLeft />
                            </div>
                            <div className="bottomCornerIcon cornerIcon">
                                <RxCornerBottomLeft />
                            </div>                </div>
                        <div style={{margin: "auto 0 auto 0", display: "flex", flexDirection: "column"}}>
                            <Button className="currencyBtn">
                                <MdCurrencyExchange className="currencyIcon" />
                                &nbsp;• Select Currency
                            </Button>
                            <Button className="locationBtn">
                                <MdOutlineLocationOn className="locationIcon" />
                                &nbsp;• Select Location
                            </Button>
                        </div>
                        <Button className="signInBtn headBtn" onClick={goToSignIn}>Sign In</Button>
                    </div>
                </div>
            </div>
            <Navigation />
        </div>
    )
};

export default Header;

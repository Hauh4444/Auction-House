// External Libraries
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, CardContent, CardHeader, FormControl, InputLabel, Select, MenuItem, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { encodeImageToBase64 } from "@/utils/helpers";

// Stylesheets
import "./SellerProfile.scss";

const SellerProfile = () => {
    return (
        <div className="sellerProfilePage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default SellerProfile;
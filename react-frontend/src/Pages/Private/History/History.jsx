// External Libraries
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, CardContent, CardHeader, FormControl, InputLabel, Select, MenuItem, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import HistoryNav from "@/Components/Navigation/HistoryNav/HistoryNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { encodeImageToBase64 } from "@/utils/helpers"

// Stylesheets
import "./History.scss"

const History = () => {


    return (
        <div className="userAccountPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <HistoryNav />
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default History;
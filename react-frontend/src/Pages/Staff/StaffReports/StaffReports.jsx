// External Libraries
import { useEffect, useState } from 'react';
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header.jsx";
import RightNav from "@/Components/Navigation/RightNav/RightNav.jsx";

const StaffReports = () => {

    return (
        <div className="staffReportsPage page">
            <div className="mainPage">
                <Header />

            </div>
            <RightNav />
        </div>
    );
};


export default StaffReports;
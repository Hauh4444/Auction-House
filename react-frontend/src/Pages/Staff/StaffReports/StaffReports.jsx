// External Libraries
import { useEffect, useState } from 'react';
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header.jsx";
import RightNav from "@/Components/Navigation/RightNav/RightNav.jsx";

const StaffReports = () => {
    const [chart, setChart] = useState("");

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/analytics/login_data/`, {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
        })
            .then((res) => setChart(res.data.chart))
            .catch((err) => console.error(err));
    }, []);

    return (
        <div className="staffReportsPage page">
            <div className="mainPage">
                <Header />
                <div
                    className="chartContainer"
                    dangerouslySetInnerHTML={ { __html: chart } }
                />
            </div>
            <RightNav />
        </div>
    );
};


export default StaffReports;
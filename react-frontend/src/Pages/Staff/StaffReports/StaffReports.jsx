// External Libraries
import { useEffect, useState } from 'react';
import axios from "axios";
import { Line } from 'react-chartjs-2';

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

const StaffReports = () => {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/admin/analytics/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then((res) => {
                setChartData({
                    labels: res.data.labels,
                    datasets: [
                        {
                            label: 'Pageviews',
                            data: res.data.data,
                            fill: false,
                            backgroundColor: 'blue',
                            borderColor: 'blue',
                        },
                    ],
                });
            })
            .catch(err => console.error(err));
    }, []);

    return (
        <div className="staffReportsPage page">
            <div className="mainPage">
                <Header />


                {chartData && (
                    <Line data={chartData} />
                )}
            </div>
            <RightNav />
        </div>
    );
};


export default StaffReports;
// External Libraries
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Card, CardContent } from "@mui/material"
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import HistoryNav from "@/Components/Navigation/HistoryNav/HistoryNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { renderStars } from "@/utils/helpers";

// Stylesheets
import "./History.scss"

const History = () => {
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL

    const [history, setHistory] = useState([]);

    useEffect(() => {
        // Fetch listings from the API with the specified filters
        axios.get(`http://127.0.0.1:5000/api/user/${filters.nav}/`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
            .then(res => setHistory(res.data[filters.nav]))
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]);

    return (
        <div className="userHistoryPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <HistoryNav />

                <div className="historyItems">
                    {history && history.map((item, index) => (
                        <>
                            <Card className="historyCard" key={index}>
                                <CardContent className="cardContent">
                                    {filters.nav === "orders" ? (
                                        <>
                                            <p><strong>Date:</strong> {item.order_date}</p>
                                            <p><strong>Status:</strong> {item.status}</p>
                                        </>
                                    ) : filters.nav === "reviews" && (
                                        <>
                                            <p><strong>Title:</strong> {item.title}</p>
                                            <p><strong>Description:</strong> {item.description}</p>
                                            <div className="review">
                                                {renderStars(item.stars)}
                                            </div>
                                        </>
                                    )}
                                </CardContent>
                            </Card>
                        < />
                    ))}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default History;
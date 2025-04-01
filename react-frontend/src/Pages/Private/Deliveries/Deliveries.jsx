// External Libraries
import { useEffect, useState } from "react";
import { Card, CardContent } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./Deliveries.scss";

const Deliveries = () => {
    const [deliveries, setDeliveries] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/user/deliveries/" , {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then((res) => setDeliveries(res.data.deliveries))
            .catch(err => console.log(err)); // Log errors if any
    }, []);

    return (
        <div className="deliveriesPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <div className="deliveryItems">
                    {deliveries.map((delivery, index) => (
                        <Card className="deliveryCard" key={index}>
                            <CardContent className="cardContent">
                                <p><strong>Address:</strong> {delivery.address}, {delivery.city}, {delivery.state}, {delivery.country}</p>
                                <p><strong>Status:</strong> {delivery.delivery_status}</p>
                                <p><strong>Tracking Number:</strong> {delivery.tracking_number}</p>
                                <p><strong>Courier:</strong> {delivery.courier}</p>
                                <p><strong>Expected Arrival Date:</strong> {delivery.estimated_delivery_date}</p>
                                {delivery.delivery_date && (
                                    <p><strong>Date Delivered:</strong> {delivery.delivery_date}</p>
                                )}
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default Deliveries;
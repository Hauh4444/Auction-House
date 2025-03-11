// External Libraries
import { useEffect, useState } from "react";
import {createSearchParams, useLocation, useNavigate} from "react-router-dom";
import {Button, Card, CardContent} from "@mui/material"
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import HistoryNav from "@/Components/Navigation/HistoryNav/HistoryNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext"
import { renderStars, navigateToListing } from "@/utils/helpers.jsx";

// Stylesheets
import "./History.scss"

const History = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL
    const auth = useAuth(); // Access authentication functions from the AuthProvider context

    const [history, setHistory] = useState([]);

    useEffect(() => {
        // Fetch listings from the API with the specified filters
        axios.get(`http://127.0.0.1:5000/api/user/${auth.user}/${filters.nav}`, {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => {
                setHistory(res.data[filters.nav]); // Set the fetched items into state
            })
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]);

    return (
        <div className="userAccountPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <HistoryNav />

                {history.map((item, index) => (
                    <div className="historyItem" key={index}>
                        {filters.nav === "orders" && (
                            <Card className="historyCard">
                                <CardContent className="cardContent">
                                    <p><strong>Date:</strong> {item.orderDate}</p>
                                    <p><strong>Status:</strong> {item.status}</p>
                                    <p><strong>Total Amount:</strong> ${item.totalAmount}</p>
                                    <p><strong>Payment Status:</strong> {item.paymentStatus}</p>
                                    <p><strong>Shipping Address:</strong> {item.shippingAddress}</p>
                                    <p><strong>Shipping Method:</strong> {item.shippingMethod}</p>
                                    <p><strong>Tracking Number:</strong> {item.trackingNumber || 'N/A'}</p>
                                    <p><strong>Shipping Cost:</strong> ${item.shippingCost}</p>
                                </CardContent>
                            </Card>
                        )}
                        {filters.nav === "transactions" && (
                            <Card className="historyCard">
                                <CardContent className="cardContent">
                                    <p><strong>Date:</strong> {item.transaction_date}</p>
                                    <p><strong>Type:</strong> {item.transaction_type}</p>
                                    <p><strong>Total Amount:</strong> {item.amount}</p>
                                    <p><strong>Payment Method:</strong> ${item.payment_method}</p>
                                </CardContent>
                            </Card>
                        )}
                        {filters.nav === "reviews" && (
                            <Card className="historyCard">
                                <CardContent className="cardContent">
                                    <p><strong>Title:</strong> {item.title}</p>
                                    <p><strong>Description:</strong> {item.description}</p>
                                    <div className="review">
                                        {/* Render the star rating based on the average review */}
                                        {renderStars(item.stars)}
                                    </div>
                                </CardContent>
                            </Card>
                        )}
                    </div>
                ))}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default History;
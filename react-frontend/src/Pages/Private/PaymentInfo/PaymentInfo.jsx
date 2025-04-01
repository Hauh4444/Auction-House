// External Libraries
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Card, CardContent } from "@mui/material"
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import PaymentNav from "@/Components/Navigation/PaymentNav/PaymentNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./PaymentInfo.scss"

const PaymentInfo = () => {
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL

    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        // Fetch listings from the API with the specified filters
        axios.get(`http://127.0.0.1:5000/api/user/${filters.nav}/`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
            .then((res) => setTransactions(res.data.transactions))
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]);

    return (
        <div className="paymentInfoPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <PaymentNav />

                {filters.nav === "transactions" && (
                    <div className="transactionItems">
                        {transactions.map((transaction, index) => (
                            <Card className="transactionCard" key={index}>
                                <CardContent className="cardContent">
                                    <p><strong>Date:</strong> {transaction.transaction_date}</p>
                                    <p><strong>Type:</strong> {transaction.transaction_type}</p>
                                    <p><strong>Total Amount:</strong> ${transaction.amount}</p>
                                    <p><strong>Payment Method:</strong> {transaction.payment_method}</p>
                                    <p><strong>Payment Status:</strong> {transaction.payment_status}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default PaymentInfo;
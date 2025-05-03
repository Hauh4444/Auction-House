// External Libraries
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import PaymentNav from "@/Components/Navigation/PaymentNav/PaymentNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import TransactionCard from "@/Components/Transaction/TransactionCard";

// Stylesheets
import "./PaymentInfo.scss"

const PaymentInfo = () => {
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL

    const [transactions, setTransactions] = useState([]);
    const [paymentMethods, setPaymentMethods] = useState({}); // To store payment method details

    useEffect(() => {
        // Fetch listings from the API with the specified filters
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/${ filters.nav }/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then((res) => {
                setTransactions(res.data.transactions);
            })
            .catch((err) => console.error(err)); // Log errors if any
    }, [location.search]);

    useEffect(() => {
        // Fetch payment method details for each transaction
        const fetchPaymentMethodDetails = async () => {
            try {
                const paymentDetails = {};
                for (let transaction of transactions) {
                    const paymentMethodId = transaction.payment_method;
                    const res = await axios.get(
                        `${ import.meta.env.VITE_BACKEND_API_URL }/purchase/payment-method/${paymentMethodId}/`
                    );
                    paymentDetails[paymentMethodId] = res.data.payment_method;
                }
                setPaymentMethods(paymentDetails);
            } catch (error) {
                console.error("Error fetching payment method details:", error);
            }
        };

        if (transactions.length > 0) {
            fetchPaymentMethodDetails();
        }
    }, [transactions]);

    return (
        <div className="paymentInfoPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <PaymentNav />

                {filters.nav === "transactions" && (
                    <div className="transactionItems">
                        {transactions.map((transaction, index) => (
                            <TransactionCard
                                key={index}
                                transaction={transaction}
                                paymentMethod={paymentMethods[transaction.payment_method]}
                            />
                        ))}
                    </div>
                )}
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
};

export default PaymentInfo;

// External Libraries
import { FaCcVisa, FaCcMastercard, FaCcAmex, FaCcDiscover, FaCcJcb, FaCcDinersClub } from "react-icons/fa"; // import the necessary card icons
import { Card, CardContent, Typography, Divider } from "@mui/material";
import PropTypes from "prop-types";

// Stylesheets
import "./TransactionCard.scss";

const TransactionCard = ({ transaction, paymentMethod }) => {
    const statusStyles = {
        succeeded: "succeeded",
        pending: "pending",
        failed: "failed",
        canceled: "canceled",
        processing: "processing",
    };

    const getStatusCard = (status) => {
        const statusKey = status.toLowerCase(); // Convert status to lowercase
        const statusClass = statusStyles[statusKey] || ""; // Get the corresponding status class

        return statusClass ? <span className={`statusCard ${statusClass}`}>{status}</span> : null;
    };

    const getCardIcon = (brand) => {
        switch (brand) {
            case "visa":
                return <FaCcVisa />;
            case "mastercard":
                return <FaCcMastercard />;
            case "amex":
                return <FaCcAmex />;
            case "discover":
                return <FaCcDiscover />;
            case "jcb":
                return <FaCcJcb />;
            case "diners":
                return <FaCcDinersClub />;
            default:
                return null;
        }
    };

    return (
        <Card className="transactionCard">
            <CardContent className="cardContent">
                <Typography variant="h6" gutterBottom>
                    Transaction: {transaction.id.slice(0, 12)}...
                </Typography>

                <Divider className="thickDivider divider" />

                <div className="infoGrid">
                    {[
                        ["Amount", `$${(transaction.amount / 100).toFixed(2)}`],
                        ["Status", getStatusCard(transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1))],
                        ["Currency", transaction.currency.toUpperCase()],
                        ["Method", transaction.confirmation_method.charAt(0).toUpperCase() + transaction.confirmation_method.slice(1)],
                    ].map(([label, value], i) => (
                        <div className="infoItem" key={i}>
                            <span className="label">{label}</span>
                            <span>{value}</span>
                        </div>
                    ))}
                </div>

                <Divider className="divider" />

                <div className="infoGrid">
                    <div className="infoItem fullWidth">
                        <span className="label">Payment</span>
                        <span>
                            {paymentMethod ? (
                                <>
                                    <span className={`card-icon ${paymentMethod.card.brand.toLowerCase()}`}>
                                        {getCardIcon(paymentMethod.card.brand.toLowerCase())}
                                    </span>
                                    ****{paymentMethod.card.last4}
                                </>
                            ) : (
                                "Loading..."
                            )}
                        </span>
                    </div>
                    <div className="infoItem fullWidth">
                        <span className="label">Created On</span>
                        <span>{new Date(transaction.created * 1000).toLocaleString()}</span>
                    </div>
                </div>

                <Divider className="divider" />

                <div className="description">
                    <strong>Description:</strong> {transaction.description || "No description provided"}
                </div>

                {transaction.metadata && (
                    <div className="metadata">
                        <strong>Metadata:</strong>
                        {Object.entries(transaction.metadata).map(([key, val], idx) => (
                            <div key={idx}>{key}: {val}</div>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    );
};

TransactionCard.propTypes = {
    transaction: PropTypes.object,
    paymentMethod: PropTypes.object,
};

export default TransactionCard;

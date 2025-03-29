// External Libraries
import { useState} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, TextField } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header.jsx";
import RightNav from "@/Components/Navigation/RightNav/RightNav.jsx";

// Stylesheets
import './Support.scss';
import axios from "axios";

const Support = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL

    const [subject, setSubject] = useState(filters.nav.charAt(0).toUpperCase() + filters.nav.slice(1));
    const [message, setMessage] = useState("");

    const cardInfo = {
        "?nav=tracking": "Where's My Shit",
        "?nav=shipping": "Shipping & Delivery",
        "?nav=product": "Returns, Refunds and Product StaffSupport",
        "?nav=account": "Managing Your Account",
        "?nav=security": "Security & Privacy",
        "?nav=payment": "Payment & Pricing",
        "?nav=report": "Report",
        "?nav=other": "Other",
    };

    const handleSubmit = () => {
        axios.post("http://127.0.0.1:5000/api/support/tickets/",
            {
                subject: subject,
                message: message,
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true,
            })
            .then(() => navigate("/"))
            .catch(error => console.error('Error submitting support ticket:', error));
    }

    return (
        <div className="supportPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <h1>Support</h1>

                {filters.nav === undefined ? (
                    <div className="supportNav">
                        {Object.keys(cardInfo).map((key, index) => (
                            <Button
                                className="navBtn"
                                onClick={() => {navigate("/user/support" + key)}}
                                key={index}
                            >
                                <h2>{cardInfo[key]}</h2>
                            </Button>
                        ))}
                    </div>
                ) : (
                    <div className="supportTicket">
                        <TextField
                            className="subject"
                            value={subject || filters.nav.charAt(0).toUpperCase() + filters.nav.slice(1)}
                            label="Subject"
                            type="text"
                            onChange={(e) => {
                                setSubject(e.target.value)
                            }}
                            variant="outlined"
                        />
                        <TextField
                            className="message"
                            value={message}
                            label="Message"
                            type="text"
                            onChange={(e) => {
                                setMessage(e.target.value)
                            }}
                            variant="outlined"
                            multiline={true}
                            rows={5}
                            maxrows={10}
                        />
                        <Button className="submitBtn" onClick={() => handleSubmit()}>Submit</Button>
                    </div>
                )}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    )
}

export default Support;
// External Libraries
import {useEffect, useState} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { Button, TextField } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header.jsx";
import RightNav from "@/Components/Navigation/RightNav/RightNav.jsx";
import { useAuth } from "@/ContextAPI/AuthContext.js";

// Stylesheets
import './Support.scss';

const Support = () => {
    const auth = useAuth();
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL

    const [subject, setSubject] = useState(null);
    const [message, setMessage] = useState("");
    const [supportTickets, setSupportTickets] = useState([]);
    const [currentSupportTicket, setCurrentSupportTicket] = useState(null);
    const [ticketMessages, setTicketMessages] = useState([]);
    const [newTicketMessage, setNewTicketMessage] = useState('');

    const cardInfo = {
        "?nav=tracking": "Where's My Shit",
        "?nav=shipping": "Shipping & Delivery",
        "?nav=product": "Returns, Refunds and Product StaffSupport",
        "?nav=account": "Managing Your Account",
        "?nav=security": "Security & Privacy",
        "?nav=payment": "Payment & Pricing",
        "?nav=tickets": "Open Support Tickets",
        "?nav=report": "Report",
        "?nav=other": "Other",
    };

    useEffect(() => {
        if (!currentSupportTicket) return;

        axios.get(`http://127.0.0.1:5000/api/ticket/messages/${currentSupportTicket.ticket_id}`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then((res) => setTicketMessages(res.data.ticket_messages))
            .catch(() => setTicketMessages([]));
    }, [currentSupportTicket]);

    const handleSelectSupport = (key) => {
        navigate("/user/support" + key);
        setSubject(key.charAt(5).toUpperCase() + key.slice(6));

        if (key.slice(5) === "tickets") {
            axios.get("http://127.0.0.1:5000/api/support/tickets", {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true, // Ensures cookies are sent with requests
            })
                .then((res) => {
                    setSupportTickets(res.data.support_tickets);
                    setCurrentSupportTicket(res.data.support_tickets[0])
                }) // Set the user state
                .catch(err => console.log(err)); // Log errors if any
        }
    }

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

    const handleSelectChat = (chat) => {
        setCurrentSupportTicket(chat);
    }

    const handleSendMessage = () => {
        if (!newTicketMessage.trim()) return;
        axios.post(`http://127.0.0.1:5000/api/ticket/messages/${currentSupportTicket.ticket_id}/`,
            {
                message: newTicketMessage
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true,
            })
            .then(() => {
                setNewTicketMessage("");

                axios.get(`http://127.0.0.1:5000/api/ticket/messages/${currentSupportTicket.ticket_id}`, {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    withCredentials: true, // Ensures cookies are sent with requests
                })
                    .then((res) => {
                        setTicketMessages(res.data.ticket_messages);
                    } )
                    .catch(err => console.log(err)); // Log errors if any
            })
            .catch(error => console.error('Error sending message:', error));
    };

    return (
        <div className="supportPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                {filters.nav === undefined ? (
                    <>
                        <h1>Support</h1>
                        <div className="supportNav">
                            {Object.keys(cardInfo).map((key, index) => (
                                <Button
                                    className="navBtn"
                                    onClick={() => handleSelectSupport(key)}
                                    key={index}
                                >
                                    <h2>{cardInfo[key]}</h2>
                                </Button>
                            ))}
                        </div>
                    </>
                ) : (filters.nav === "tickets" ? (
                        <div className="content">
                            <div className="supportTickets">
                                {supportTickets && supportTickets.map((ticket, index) => (
                                    <Button className={`ticket${currentSupportTicket === ticket ? " selected" : ""}`} key={index} onClick={() => handleSelectChat(ticket)}>
                                        {ticket.subject}
                                    </Button>
                                ))}
                            </div>
                            <div className="main">
                                <div className="messages">
                                    {ticketMessages && ticketMessages.map((ticketMessage, index) => (
                                        <div className={`message${auth.user.user_id === ticketMessage.sender_id ? " thisUser" : ""}`} key={index}>
                                            {ticketMessage.message}
                                        </div>
                                    ))}
                                </div>
                                <div className="newMessage">
                                    <TextField
                                        className="input"
                                        value={newTicketMessage}
                                        label="Message"
                                        type="text"
                                        onChange={(e) => setNewTicketMessage(e.target.value)}
                                        variant="outlined"
                                        sx={{
                                            '& .MuiOutlinedInput-root': {
                                                borderRadius: '25px', // Set the border radius
                                            },
                                        }}
                                    />
                                    <Button className="btn" onClick={() => handleSendMessage()}>Send</Button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <>
                            <h1>Support</h1>
                            <div className="supportTicket">
                                <TextField
                                    className="subject"
                                    value={subject}
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
                        </>
                    )
                )}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    )
}

export default Support;
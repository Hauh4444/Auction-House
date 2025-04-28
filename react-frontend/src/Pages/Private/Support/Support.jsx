// External Libraries
import {useEffect, useLayoutEffect, useRef, useState} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import { Button, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext";

// Stylesheets
import './Support.scss';

const Support = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL
    const auth = useAuth(); // Fetch the authentication context

    const [subject, setSubject] = useState(null);
    const [message, setMessage] = useState("");
    const [supportTickets, setSupportTickets] = useState([]);
    const [currentSupportTicket, setCurrentSupportTicket] = useState(null);
    const [ticketMessages, setTicketMessages] = useState([]);
    const [newTicketMessage, setNewTicketMessage] = useState('');

    const messagesEndRef = useRef(null); // Reference to scroll to the bottom of the messages div
    const currentSupportTicketRef = useRef(currentSupportTicket);

    useEffect(() => {
        currentSupportTicketRef.current = currentSupportTicket;
    }, [currentSupportTicket]);

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

    const getMessages = () => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/ticket/messages/${ currentSupportTicket.ticket_id }/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => setTicketMessages(res.data.ticket_messages))
            .catch(() => setTicketMessages([]));
    }

    useEffect(() => {
        if (!currentSupportTicket) return;
        getMessages();
    }, [currentSupportTicket]);

    // Scroll to the bottom of the messages list after new messages are loaded or after sending a new message
    useLayoutEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
        }
    }, [ticketMessages]); // This will trigger scroll whenever messages change

    useEffect(() => {
        const socket = io(import.meta.env.VITE_BACKEND_URL, {
            transports: ["websocket"],
            withCredentials: true,
        });

        if (!socket) return;

        // We have to use references because of fucking race conditions
        const handleNewMessage = () => {
            const ticketId = currentSupportTicketRef.current?.ticket_id;
            if (ticketId) {
                axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/ticket/messages/${ ticketId }/`,
                    {
                        headers: { "Content-Type": "application/json" },
                        withCredentials: true, // Ensures cookies are sent with requests
                    })
                    .then((res) => setTicketMessages(res.data.ticket_messages))
                    .catch(() => setTicketMessages([]));
            }
        }

        socket.on("new_ticket_message", handleNewMessage);

        return () => {
            socket.off("new_ticket_message", handleNewMessage);
        };
    }, []);

    const handleSelectSubject = (key) => {
        navigate("/user/support" + key);
        setSubject(key.charAt(5).toUpperCase() + key.slice(6));

        if (key.slice(5) === "tickets") {
            axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/support/tickets/`,
                {
                    headers: { "Content-Type": "application/json" },
                    withCredentials: true, // Ensures cookies are sent with requests
                })
                .then((res) => {
                    setSupportTickets(res.data.support_tickets);
                    setCurrentSupportTicket(res.data.support_tickets[0])
                }) // Set the user state
                .catch((err) => console.error(err)); // Log errors if any
        }
    }

    const handleSubmitTicket = () => {
        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/support/tickets/`,
            {
                subject: subject,
                message: message,
            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => navigate("/"))
            .catch((err) => console.error(err));
    }

    const handleSendMessage = () => {
        if (!newTicketMessage.trim()) return;
        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/ticket/messages/${ currentSupportTicket.ticket_id }/`,
            {
                message: newTicketMessage
            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => {
                setNewTicketMessage("");
                getMessages();
            })
            .catch((err) => console.error(err));
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <div className="supportPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                {filters.nav === undefined ? (
                    <>
                        <h1>Support</h1>
                        <div className="supportNav">
                            {Object.keys(cardInfo).map((key, index) => (
                                <Button
                                    className="navBtn"
                                    onClick={ () => handleSelectSubject(key) }
                                    key={ index }
                                >
                                    <h2>{ cardInfo[key] }</h2>
                                </Button>
                            ))}
                        </div>
                    </>
                ) : (filters.nav === "tickets" ? (
                        <div className="content">
                            <div className="supportTickets">
                                {supportTickets && supportTickets.map((ticket, index) => (
                                    <Button
                                        className={ `ticket${ currentSupportTicket === ticket ? " selected" : ""  }`}
                                        key={ index }
                                        onClick={ () => setCurrentSupportTicket(ticket) }
                                    >
                                        { ticket.subject }
                                    </Button>
                                ))}
                            </div>
                            <div className="main">
                                <div className="messages">
                                    {ticketMessages && ticketMessages.map((ticketMessage, index) => (
                                        <div className={ `message${ auth.user.user_id === ticketMessage.sender_id ? " thisUser" : ""  }`} key={ index }>
                                            { ticketMessage.message }
                                        </div>
                                    ))}
                                    <div ref={ messagesEndRef } />
                                </div>
                                <div className="newMessage">
                                    <TextField
                                        className="input"
                                        value={ newTicketMessage }
                                        label="Message"
                                        type="text"
                                        onChange={ (e) => setNewTicketMessage(e.target.value) }
                                        onKeyDown={ (e) => handleKeyPress(e) }
                                        variant="outlined"
                                        sx={{
                                            '& .MuiOutlinedInput-root': {
                                                borderRadius: '25px',
                                            },
                                        }}
                                    />
                                    <Button className="btn" onClick={ () => handleSendMessage() }>Send</Button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <>
                            <h1>Support</h1>
                            <div className="supportTicket">
                                <TextField
                                    className="subject"
                                    value={ subject }
                                    label="Subject"
                                    type="text"
                                    onChange={(e) => {
                                        setSubject(e.target.value)
                                    }}
                                    variant="outlined"
                                />
                                <TextField
                                    className="message"
                                    value={ message }
                                    label="Message"
                                    type="text"
                                    onChange={(e) => {
                                        setMessage(e.target.value)
                                    }}
                                    variant="outlined"
                                    multiline={ true }
                                    rows={ 5 }
                                    maxrows={ 10 }
                                />
                                <Button className="submitBtn" onClick={ () => handleSubmitTicket() }>Submit</Button>
                            </div>
                        </>
                    )
                )}
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    )
}

export default Support;
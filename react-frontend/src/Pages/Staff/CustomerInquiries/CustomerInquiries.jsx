// External Libraries
import { useState, useEffect, useRef, useLayoutEffect } from 'react';
import { io } from "socket.io-client";
import { Button, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext";

// Stylesheets
import "./CustomerInquiries.scss"

const CustomerInquiries = () => {
    const auth = useAuth(); // Fetch the authentication context

    const [supportTickets, setSupportTickets] = useState([]);
    const [currentSupportTicket, setCurrentSupportTicket] = useState(null);
    const [ticketMessages, setTicketMessages] = useState([]);
    const [newTicketMessage, setNewTicketMessage] = useState('');

    const messagesEndRef = useRef(null); // Reference to scroll to the bottom of the messages div
    const currentSupportTicketRef = useRef(currentSupportTicket);

    useEffect(() => {
        currentSupportTicketRef.current = currentSupportTicket;
    }, [currentSupportTicket]);

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/support/tickets/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => {
                setSupportTickets(res.data.support_tickets);
                setCurrentSupportTicket(res.data.support_tickets[0])
            })
            .catch(err => console.error(err)); // Log errors if any
    }, []);

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
        const socket = io(import.meta.env.VITE_BACKEND_URL, {
            transports: ["websocket"],
            withCredentials: true,
        });

        if (!socket) return;

        // We have to use references because of fucking race conditions
        const handleNewMessage = () => {
            const ticketId = currentSupportTicketRef.current?.ticket_id;
            if (ticketId) {
                axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/ticket/messages/${ ticketId }/`,
                    {
                        headers: {"Content-Type": "application/json"},
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
            .catch(err => console.error(err));
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <div className="customerInquiriesPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

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
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
}

export default CustomerInquiries;
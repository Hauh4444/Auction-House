// External Libraries
import { useState, useEffect } from 'react';
import axios from "axios";
import { Button, TextField } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext";

// Stylesheets
import "./CustomerInquiries.scss"

const CustomerInquiries = () => {
    const auth = useAuth();

    console.log(auth.user.user_id)

    const [supportTickets, setSupportTickets] = useState([]);
    const [currentSupportTicket, setCurrentSupportTicket] = useState(null);
    const [ticketMessages, setTicketMessages] = useState([]);
    const [newTicketMessage, setNewTicketMessage] = useState('');

    useEffect(() => {
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
    }, []);

    useEffect(() => {
        if (!currentSupportTicket) return;

        axios.get(`http://127.0.0.1:5000/api/ticket/messages/${currentSupportTicket.ticket_id}`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then((res) => {
                setTicketMessages(res.data.ticket_messages); // Set the user state
            } )
            .catch(() => setTicketMessages([]));
    }, [currentSupportTicket]);

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
                        setTicketMessages(res.data.ticket_messages); // Set the user state
                    } )
                    .catch(err => console.log(err)); // Log errors if any
            })
            .catch(error => console.error('Error sending message:', error));
    };

    return (
        <div className="customerInquiriesPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

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
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default CustomerInquiries;
// External Libraries
import { useState, useEffect, useRef } from 'react';
import { Button, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import SocketProvider from "@/ContextAPI/SocketProvider";
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext";
import { useSocket } from "@/ContextAPI/SocketContext";

// Stylesheets
import "./CustomerInquiries.scss"

const CustomerInquiries = () => {
    const auth = useAuth();
    const socket = useSocket();

    const [supportTickets, setSupportTickets] = useState([]);
    const [currentSupportTicket, setCurrentSupportTicket] = useState(null);
    const [ticketMessages, setTicketMessages] = useState([]);
    const [newTicketMessage, setNewTicketMessage] = useState('');

    const messagesEndRef = useRef(null); // Reference to scroll to the bottom of the messages div

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/support/tickets/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => {
                setSupportTickets(res.data.support_tickets);
                setCurrentSupportTicket(res.data.support_tickets[0])
            }) // Set the user state
            .catch(err => console.error(err)); // Log errors if any
    }, []);

    const getMessages = () => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/ticket/messages/${ currentSupportTicket.ticket_id }/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => {
                setTicketMessages(res.data.ticket_messages);
                // Scroll to the bottom of the messages container after the messages are updated
                if (messagesEndRef.current) {
                    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
                }
            })
            .catch(() => setTicketMessages([]));
    }

    useEffect(() => {
        if (!currentSupportTicket) return;
        getMessages();
    }, [currentSupportTicket]);

    useEffect(() => {
        if (!socket.current || !currentSupportTicket) return; // Return if socket or currentSupportTicket is not available
        socket.current.on("new_ticket_message", getMessages); // Fetch ticket messages on new_ticket_message event

        return () => {
            if (socket.current) {
                socket.current.off("new_message", getMessages); // Clean up the event listener on component unmount
            }
        };
    }, [socket, currentSupportTicket]);

    const handleSelectTicket = (chat) => {
        setCurrentSupportTicket(chat);
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
            .catch(err => console.error(err));
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <SocketProvider>
            <div className="customerInquiriesPage page">
                <div className="mainPage">
                    { /* Page Header */ }
                    <Header />

                    <div className="content">
                        <div className="supportTickets">
                            {supportTickets && supportTickets.map((ticket, index) => (
                                <Button className={ `ticket${ currentSupportTicket === ticket ? " selected" : ""  }`} key={ index } onClick={ () => handleSelectTicket(ticket) }>
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
                                    onKeyDown={ handleKeyPress }
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
        </SocketProvider>
    );
}

export default CustomerInquiries;
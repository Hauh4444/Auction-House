// External Libraries
import { useState, useEffect, useRef, useLayoutEffect } from "react";
import { io } from "socket.io-client";
import { Button, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext";

// Stylesheets
import "./Messages.scss";

const Messages = () => {
    const auth = useAuth();

    const [chats, setChats] = useState([]); // State for storing chats
    const [currentChat, setCurrentChat] = useState(null); // State for the currently selected chat
    const [messages, setMessages] = useState([]); // State for storing messages of the current chat
    const [newMessage, setNewMessage] = useState(""); // State for storing new message input

    const messagesEndRef = useRef(null); // Reference to scroll to the bottom of the messages div

    // Fetch chats and set the first chat as current chat
    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/chats/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => {
                setChats(res.data.chats); // Set the chats state
                setCurrentChat(res.data.chats[0]) // Set the first chat as the current chat
            })
            .catch(() => setChats([])); // Log errors if any
    }, []);

    // Fetch messages for the current chat
    const getMessages = () => {
        if (!currentChat) return;
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/messages/${ currentChat.chat_id }/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => {
                setMessages(res.data.messages); // Set the messages state
            })
            .catch(() => setMessages([]));
    };

    useEffect(() => {
        const socket = io(import.meta.env.VITE_BACKEND_URL, {
            transports: ["polling"],
            withCredentials: true,
        });

        if (!socket) return;

        socket.on("new_message", getMessages);

        return () => {
            socket.off("new_message", getMessages);
        };
    }, []);

    // When current chat changes, fetch messages for the new chat
    useEffect(() => {
        if (!currentChat) return;
        getMessages();
    }, [currentChat]);

    // Scroll to the bottom of the messages list after new messages are loaded or after sending a new message
    useLayoutEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
        }
    }, [messages]); // This will trigger scroll whenever messages change

    const handleSendMessage = () => {
        if (!newMessage.trim()) return; // Prevent sending empty messages
        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/user/messages/${ currentChat.chat_id }/`, {
            message: newMessage
        }, {
            headers: { "Content-Type": "application/json" },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(() => {
                setNewMessage(""); // Reset message input
                getMessages(); // Fetch new messages
            })
            .catch(err => console.error(err)); // Log errors if any
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter") {
            handleSendMessage();
        }
    };

    return (
        <div className="messagesPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <div className="content">
                    <div className="chats">
                        {chats && chats.map((chat, index) => (
                            <Button
                                className={ `chat${ currentChat === chat ? " selected" : ""  }`}
                                key={ index }
                                onClick={ () => setCurrentChat(chat) }
                            >
                                Chat { index + 1 }
                            </Button>
                        ))}
                        <Button className="createChat" onClick={ () => handleCreateChat() }>
                            New Chat
                        </Button>
                    </div>
                    <div className="main">
                        <div className="messages">
                            {messages && messages.map((message, index) => (
                                <div className={ `message${ auth.user.user_id === message.sender_id ? " thisUser" : ""  }`} key={ index }>
                                    { message.message }
                                </div>
                            ))}
                            <div ref={messagesEndRef} /> {/* Scroll target */}
                        </div>
                        <div className="newMessage">
                            <TextField
                                className="input"
                                value={newMessage}
                                label="Message"
                                type="text"
                                onChange={(e) => setNewMessage(e.target.value)}
                                onKeyDown={handleKeyPress}
                                variant="outlined"
                                sx={{
                                    "& .MuiOutlinedInput-root": {
                                        borderRadius: "25px",
                                    },
                                }}
                            />
                            <Button className="btn" onClick={handleSendMessage}>Send</Button>
                        </div>
                    </div>
                </div>
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
};

export default Messages;

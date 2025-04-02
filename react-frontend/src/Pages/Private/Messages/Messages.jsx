// External Libraries
import { useState, useEffect } from 'react';
import axios from "axios";
import { Button, TextField } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { useAuth } from "@/ContextAPI/AuthContext.js";

// Stylesheets
import './Messages.scss';

const Messages = () => {
    const auth = useAuth();

    const [chats, setChats] = useState([]);
    const [currentChat, setCurrentChat] = useState(null);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/user/chats/", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then((res) => {
                setChats(res.data.chats);
                setCurrentChat(res.data.chats[0])
            }) // Set the user state
            .catch(err => console.log(err)); // Log errors if any
    }, []);

    useEffect(() => {
        if (!currentChat) return;

        axios.get(`http://127.0.0.1:5000/api/user/messages/${currentChat.chat_id}/`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then((res) => setMessages(res.data.messages))
            .catch(() => setMessages([])); // Log errors if any
    }, [currentChat]);

    const handleCreateChat = () => {

    }

    const handleSendMessage = () => {
        if (!newMessage.trim()) return;
        axios.post(`http://127.0.0.1:5000/api/user/messages/${currentChat.chat_id}/`,
            {
                message: newMessage
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true,
            })
            .then(() => {
                setNewMessage("");

                axios.get(`http://127.0.0.1:5000/api/user/messages/${currentChat.chat_id}`, {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    withCredentials: true, // Ensures cookies are sent with requests
                })
                    .then((res) => {
                        setMessages(res.data.messages);
                    } )
                    .catch(err => console.log(err)); // Log errors if any
            })
            .catch(error => console.error('Error sending message:', error));
    };

    return (
        <div className="messagesPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <div className="content">
                    <div className="chats">
                        {chats && chats.map((chat, index) => (
                            <Button className={`chat${currentChat === chat ? " selected" : ""}`} key={index} onClick={() => setCurrentChat(chat)}>
                                Chat {index + 1}
                            </Button>
                        ))}
                        <Button className="createChat" onClick={() => handleCreateChat()}>
                            New Chat
                        </Button>
                    </div>
                    <div className="main">
                        <div className="messages">
                            {messages && messages.map((message, index) => (
                                <div className={`message${auth.user.user_id === message.sender_id ? " thisUser" : ""}`} key={index}>
                                    {/* needs to have check if sender_id is viewing user or other user */}
                                    {message.message}
                                </div>
                            ))}
                        </div>
                        <div className="newMessage">
                            <TextField
                                className="input"
                                value={newMessage}
                                label="Message"
                                type="text"
                                onChange={(e) => setNewMessage(e.target.value)}
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
    )
}

export default Messages;
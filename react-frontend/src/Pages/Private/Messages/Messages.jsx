// External Libraries
import { useState, useEffect } from 'react';
import axios from "axios";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header.jsx";
import RightNav from "@/Components/Navigation/RightNav/RightNav.jsx";

// Stylesheets
import './Messages.scss';

const Messages = () => {
    const [chats, setChats] = useState([]);
    const [messages, setMessages] = useState([]);
    const [currentChat, setCurrentChat] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/user/chats", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => setChats(res.data.chats)) // Set the user state
            .catch(err => console.log(err)); // Log errors if any
    }, []);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/user/messages/" + currentChat.chat_id, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => setMessages(res.data.messages)) // Set the user state
            .catch(err => console.log(err)); // Log errors if any
    }, [currentChat]);

    return (
        <div className="messagesPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <div className="chats">
                    {chats.map((chat, index) => (
                        <Button className="chat" key={index} onClick={() => setCurrentChat(chat)}>
                            {chat.other_user}
                        </Button>
                    ))}
                </div>
                <div className="messages">
                    {messages.map((message, index) => (
                        <div className="message" key={index}>
                            {/* needs to have check if sender_id is viewing user or other user */}
                            {message.message}
                        </div>
                    ))}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    )
}

export default Messages;
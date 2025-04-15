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
import './Messages.scss';

const Messages = () => {
    const auth = useAuth();
    const socket = useSocket();

    const [chats, setChats] = useState([]); // State for storing chats
    const [currentChat, setCurrentChat] = useState(null); // State for the currently selected chat
    const [messages, setMessages] = useState([]); // State for storing messages of the current chat
    const [newMessage, setNewMessage] = useState(''); // State for storing new message input

    const messagesEndRef = useRef(null); // Reference to scroll to the bottom of the messages div

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
            .catch(err => console.error(err)); // Log errors if any
    }, []);

    const getMessages = () => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/messages/${ currentChat.chat_id }/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => {
                setMessages(res.data.messages); // Set the messages state
                // Scroll to the bottom of the messages container after the messages are updated
                if (messagesEndRef.current) {
                    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
                }
            })
            .catch(() => setMessages([]));
    }

    useEffect(() => {
        if (!currentChat) return; // Return if no chat is selected
        getMessages() // Fetch the messages for the selected chat
    }, [currentChat]);

    useEffect(() => {
        if (!socket || !currentChat) return; // Return if socket or currentChat is not available
        socket.current.on("new_message", getMessages); // Fetch messages on new_message event

        return () => {
            if (socket) {
                socket.current.off("new_message", getMessages); // Clean up the event listener on component unmount
            }
        };
    }, [socket, currentChat]);

    useEffect(() => {
        if (!socket || !currentChat) return; // Return if socket or currentChat is not available
        socket.current.on("new_message", getMessages); // Fetch messages on new_message event

        return () => {
            if (socket) {
                socket.current.off("new_message", getMessages); // Clean up the event listener on component unmount
            }
        };
    }, [socket, currentChat]);

    const handleCreateChat = () => {

    }

    const handleSendMessage = () => {
        if (!newMessage.trim()) return; // Prevent sending empty messages
        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/user/messages/${ currentChat.chat_id }/`,
            {
                message: newMessage
            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then(() => {
                setNewMessage("");
                getMessages();
            })
            .catch(err => console.error(err)); // Log errors if any
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <SocketProvider>
            <div className="messagesPage page">
                <div className="mainPage">
                    { /* Page Header */ }
                    <Header />

                    <div className="content">
                        <div className="chats">
                            {chats && chats.map((chat, index) => (
                                <Button className={ `chat${ currentChat === chat ? " selected" : ""  }`} key={ index } onClick={ () => setCurrentChat(chat) }>
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
                                <div ref={ messagesEndRef } />
                            </div>
                            <div className="newMessage">
                                <TextField
                                    className="input"
                                    value={ newMessage }
                                    label="Message"
                                    type="text"
                                    onChange={ (e) => setNewMessage(e.target.value) }
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

export default Messages;

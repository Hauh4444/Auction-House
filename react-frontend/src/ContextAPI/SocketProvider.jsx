// External Libraries
import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

// Internal Modules
import { SocketContext } from './SocketContext';
import PropTypes from "prop-types";

const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const socketInstance = io(import.meta.env.VITE_BACKEND_API_URL, {
            transports: ['websocket'],
            withCredentials: true,
        });

        setSocket(socketInstance);

        return () => {
            if (socketInstance) {
                socketInstance.disconnect();
            }
        };
    }, []);

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};

SocketProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

export default SocketProvider;
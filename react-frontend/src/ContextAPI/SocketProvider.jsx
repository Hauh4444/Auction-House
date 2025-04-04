// External Libraries
import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

// Internal Modules
import { SocketContext } from './SocketContext';
import PropTypes from "prop-types";

const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const socketInstance = io("http://127.0.0.1:5000", {
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
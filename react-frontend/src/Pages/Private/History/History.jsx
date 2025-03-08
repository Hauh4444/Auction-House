// External Libraries
import { useEffect, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import HistoryNav from "@/Components/Navigation/HistoryNav/HistoryNav";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { encodeImageToBase64 } from "@/utils/helpers"
import { useAuth } from "@/ContextAPI/AuthContext"

// Stylesheets
import "./History.scss"

const History = () => {
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from URL
    const auth = useAuth(); // Access authentication functions from the AuthProvider context

    const [history, setHistory] = useState([]);

    useEffect(() => {
        // Fetch listings from the API with the specified filters
        axios.get(`http://127.0.0.1:5000/api/user/${auth.user}/${filters.nav}`, {
            headers: {
                "Content-Type": "application/json",
            },
            params: createSearchParams(filters), // Convert filters to query parameters
        })
            .then(res => setHistory(res.data.items)) // Set the fetched listings into state
            .catch(err => console.log(err)); // Log errors if any
    }, [location.search]);


    return (
        <div className="userAccountPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <HistoryNav />
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default History;
// External Libraries
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, TextField } from "@mui/material";
import axios from "axios";
import PropTypes from "prop-types";

// Internal Modules
import { useAuth } from "@/ContextAPI/AuthContext"

// Stylesheets
import "./LiveAuction.scss";

const LiveAuction = ({ listing }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const auth = useAuth();

    const [newBid, setNewBid] = useState((listing.current_price + 1).toFixed(2));
    const [error, setError] = useState(false);

    useEffect(() => setNewBid((listing.current_price + 1).toFixed(2)), [listing]);

    const placeBid = () => {
        if (!newBid || newBid < listing.current_price + 1) {
            setError(true);
            return;
        }
        setError(false);
        if (!auth.user) navigate("/auth-page", { state: { from: location } });

        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/bids/`,
            {
                listing_id: listing.listing_id,
                amount: newBid,
            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => alert(`New bid placed for $${newBid}`))
            .catch((err) => console.error(err));
    }

    return (
        <div className="overlay">
            <div className="liveAuction">
                <div className="section left">
                    <div className="image">
                        <img
                            src={ `data:image/jpg;base64,${ listing.image_encoded  }`}
                            alt={ listing.title }
                            style={ { display: "block" } }
                        />
                    </div>

                    <div className="currentBid">
                        <p style={ { fontSize: "25px" } }>Current bid:</p>
                        <p style={ { fontSize: "30px" } }>${ listing.current_price.toFixed(2) }</p>
                    </div>
                </div>

                <div className="divider" />

                <div className="section right">
                    <h2>Place New Bid</h2>

                    <TextField
                        className="newBid"
                        value={ newBid }
                        label="New Bid"
                        type="number"
                        onChange={ (e) => setNewBid(e.target.value) }
                        error={ error }
                        helperText={ error ? `Price must be at least ${ (listing.current_price + 1).toFixed(2) }` : "" }
                        slotProps={{ inputProps: { min: (listing.current_price + 1).toFixed(2), step: 1 } }}
                        variant="outlined"
                    />

                    <TextField
                        className="newBid"
                        value=""
                        label="Starting Bid"
                        type="number"
                        onChange={ (e) => {} }
                        variant="outlined"
                    />

                    <TextField
                        className="newBid"
                        value=""
                        label="Maximum Bid"
                        type="number"
                        onChange={ (e) => {} }
                        variant="outlined"
                    />

                    <Button className="btn" onClick={ () => placeBid() }>Submit</Button>
                </div>
            </div>
        </div>
    )
}

LiveAuction.propTypes = {
    listing: PropTypes.object.isRequired,
};

export default LiveAuction;
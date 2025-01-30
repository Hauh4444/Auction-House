import Header from "../../Components/Header/Header.jsx";
import { useState, useEffect } from 'react';
import { useLocation } from "react-router-dom";
import { Button } from "@mui/material";
import axios from 'axios';
import './Listing.scss';

const Listing = () => {
    const [listing, setListing] = useState({});
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/listings/' + queryParams.get('key'), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(res => {
                setListing(res.data.listing);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    return (
        <>
            <Header />
            <div className="listingsContainer">
                <div className="listing">
                    <div className="listingImage">
                        <img src={'data:image/jpg;base64,' + listing.image} alt="" />
                    </div>
                    <div className="listingDescription">
                        <Button className="listingTitle">
                            {listing.title}
                        </Button>
                        <h1 className="listingPrice">
                            ${listing.price}
                        </h1>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Listing;
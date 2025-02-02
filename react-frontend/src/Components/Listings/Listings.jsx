import { useState, useEffect } from 'react';
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import axios from 'axios';
import "./Listings.scss";

const Listings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);


    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/listings', {
            headers: {
                'Content-Type': 'application/json',
            },
            c: queryParams.get('c'),
        })
            .then(res => {
                setListings(res.data.listings);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    function navigateToListing(listing) {
        navigate({
            pathname: '/listings',
            search: createSearchParams({
                key: listing.id
            }).toString(),
        });
    }

    return (
        <div className="listingsContainer">
            {listings.map((listing, index) => (
                <div className="listing" key={index}>
                    <div className="listingImage">
                        <img src={'data:image/jpg;base64,' + listing.image} alt="" />
                    </div>
                    <div className="listingDescription">
                        <Button className="listingTitle" onClick={() => navigateToListing(listing)}>
                            {listing.title}
                        </Button>
                        <h1 className="listingPrice">
                            ${listing.price}
                        </h1>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Listings;
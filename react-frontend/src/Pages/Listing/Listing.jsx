// External Libraries
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
// Stylesheets
import "./Listing.scss";


const Listing = () => {
    const [listing, setListing] = useState({}); // State to store listing data
    const location = useLocation(); // Accessing the current location object from react-router-dom

    // useEffect hook to fetch listing data from the API when the component mounts
    useEffect(() => {
        const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

        // Sending GET request to fetch a specific listing based on the 'key' query parameter in the URL
        axios.get("http://127.0.0.1:5000/api/listings/" + filters.key, {
            headers: {
                "Content-Type": "application/json", // Setting the request content type to JSON
            },
        })
            .then(res => setListing(res.data))
            .catch(err => console.log(err));
    }, [location.search]); // Empty dependency array means this effect will run only once when the component mounts

    return (
        <div className="listingPage">
            <div className="mainPage">
                <Header />
                <div className="listing">
                    <div className="main">
                        <div className="info">
                            <div className="title">{listing.title}</div>
                            {listing.listing_type === "auction" ? (
                                <>
                                    <div className="bid">${listing.current_price}</div>
                                    <Button className="placeBidBtn">Place Bid</Button>
                                    <p className="bidDescription">{listing.bids} bids. Ends: {listing.auction_end}</p>
                                    <div className="price">${listing.buy_now_price}</div>
                                    <Button className="addCartBtn">Add to Cart</Button>
                                </>
                            ) : (
                                <>
                                    <div className="price">${listing.buy_now_price}</div>
                                    <Button className="addCartBtn">Add to Cart</Button>
                                </>
                            )}
                        </div>
                        <div className="image">
                            {/* Checking if image data exists; if yes, displaying image, otherwise a fallback message */}
                            {listing.image_encoded ? (
                                <img src={"data:image/jpg;base64," + listing.image_encoded} alt={listing.title} />
                            ) : (
                                <div>No image available</div>
                            )}
                        </div>
                        <div className="description">
                            <div className="title">Description:</div>
                            {/* If the description is an array and has data, display it as a list */}
                            {listing.description &&
                            Array.isArray(JSON.parse(listing.description)) &&
                            JSON.parse(listing.description).length > 0 ? (
                                <ul className="list">
                                    {JSON.parse(listing.description).map((desc, i) => (
                                        <li key={i}>{desc}</li>
                                    ))}
                                </ul>
                            ) : (
                                <div>No description available</div> // Fallback message if no description is available
                            )}
                        </div>
                    </div>
                    <div className="lesserInfo">
                        <div className="specifics">
                            {listing.item_specifics &&
                            JSON.parse(listing.item_specifics) instanceof Object ? (
                                !Array.isArray(JSON.parse(listing.item_specifics)) ? (
                                    <table>
                                        <caption>Item Specifics</caption>
                                        {Object.keys(JSON.parse(listing.item_specifics)).map((key, index) =>
                                            <tr key={index}>
                                                <th>{key}</th>
                                                <td>{JSON.parse(listing.item_specifics)[key]}</td>
                                            </tr>
                                        )}
                                    </table>
                                ) : (
                                    <></>
                                )
                            ) : (
                                <></>
                            )}
                        </div>
                        <div className="reviews">

                        </div>
                    </div>
                </div>
            </div>
            <RightNavigation />
        </div>
    )
}

export default Listing;
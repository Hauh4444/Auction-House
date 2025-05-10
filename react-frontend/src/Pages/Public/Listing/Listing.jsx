// External Libraries
import { useEffect, useState, useRef } from  "react";
import { useLocation } from "react-router-dom";
import { FacebookIcon, FacebookShareButton, PinterestIcon, PinterestShareButton, TwitterShareButton, XIcon } from "react-share";
import { IoMdCube } from "react-icons/io";
import { ImCross } from "react-icons/im";
import { io } from "socket.io-client";
import { Button } from "@mui/material";
import { format } from 'date-fns';
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc"
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import Listing3D from "@/Components/Listing3D/Listing3D";
import LiveAuction from "@/Components/Auction/LiveAuction"
import { renderStars } from "@/utils/helpers";
import { useCart } from "@/ContextAPI/CartContext";

// Stylesheets
import "./Listing.scss";

const parseJsonSafe = (str) => {
    try {
        return JSON.parse(str);
    } catch (e) {
        return null; // Return null if parsing fails
    }
};
/**
 * Listing Component
 *
 * This component fetches and displays a listing based on query parameters from the URL.
 *
 * Features:
 * - Retrieves listing data from the Flask server using Axios.
 * - Displays listing details using child components.
 * - Includes a navigation bar and header.
 *
 * @returns { JSX.Element } The rendered homepage containing the header, navigation, and conditionally rendered category navigation.
 */
const Listing = () => {
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from the URL
    const { addToCart } = useCart(); // Access authentication functions from the AuthProvider context

    const [listing, setListing] = useState({}); // State to store the listing data
    const [reviews, setReviews] = useState([]);
    const [model, setModel] = useState(null);
    const [showModel, setShowModel] = useState(false);
    const [showAuction, setShowAuction] = useState(false);

    const listingRef = useRef(listing);

    dayjs.extend(utc);

    useEffect(() => {
        listingRef.current = listing;
    }, [listing]);

    useEffect(() => getListing(), [location.search]); // Call on update of URL filters

    useEffect(() => {
        if (showModel || showAuction) document.body.style.overflow = "hidden";
        else document.body.style.overflow = "auto";

        return () => document.body.style.overflow = "auto";
    }, [showModel, showAuction]);

    useEffect(() => {
        const socket = io(import.meta.env.VITE_BACKEND_URL, {
            transports: ["websocket"],
            withCredentials: true,
        });

        if (!socket) return;

        // We have to use references because of fucking race conditions
        const handleNewBid = () => {
            const listingId = listingRef.current?.listing_id;
            if (listingId) {
                axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/${ listingId }/`,
                    {
                        headers: { "Content-Type": "application/json" },
                    })
                    .then((res) => setListing(res.data.listing)) // Update state with fetched data
                    .catch((err) => console.error(err)); // Log errors if any
            }
        }

        socket.on("new_bid", handleNewBid);

        return () => {
            socket.off("new_bid", handleNewBid);
        };
    }, []);

    useEffect(() => {
        if (showAuction || showModel) {
            const handleEscapeKey = (event) => {
                if (event.key === "Escape") {
                    if (showModel) setShowModel(false);
                    else setShowAuction(false);
                }
            };
            window.addEventListener("keydown", handleEscapeKey);

            return () => {
                window.removeEventListener("keydown", handleEscapeKey);
            };
        }
    }, [showAuction, showModel]);

    const getListing = () => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/${ filters.key }/`,
            {
                headers: { "Content-Type": "application/json" },
            })
            .then((res) => {
                setListing(res.data.listing);
                getListingObjects(res.data.listing.listing_id);
            })
            .catch((err) => console.error(err)); // Log errors if any
    }

    const getListingObjects = (id) => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/reviews/`,
            {
                headers: { "Content-Type": "application/json" },
                params: {
                    listing_id: id, // Apply listing_id parameter
                    sort: "stars", // Sort by number of stars
                    order: "desc", // Order in descending order
                    start: 0, // Start from the first item
                    range: 3, // Limit to 3 items
                },
            })
            .then((res) => setReviews(res.data.reviews)) // Update state with fetched data
            .catch(() => setReviews([])); // Clear review state on error

        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/models/listing/${ id }`,
            {
                headers: { "Content-Type": "application/json" },
            })
            .then((res) => setModel(res.data.model)) // Update state with fetched data
            .catch(() => setModel(null)); // Clear model state on error
    }

    const getParsedDescription = () => {
        const parsedDescription = parseJsonSafe(listing.description);
        if (parsedDescription === null) {
            return listing.description; // If it's not a valid JSON string, return the original description
        }
        return parsedDescription;
    };

    const getParsedItemSpecifics = () => {
        const parsedItemSpecifics = parseJsonSafe(listing.item_specifics);
        if (parsedItemSpecifics === null) {
            return listing.item_specifics; // If it's not a valid JSON string, return the original item specifics
        }
        return parsedItemSpecifics;
    };

    return (
        <div className="listingPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />
                <div className="listing">
                    { /* Main listing details */ }
                    <div className="main">
                        <div className="info">
                            { /* Display product title */ }
                            <div className="title">{ listing.title }</div>

                            { /* Display buy-now price */ }
                            <div className="buySection">
                                <div className="price">
                                    {listing?.buy_now_price ? `$${listing.buy_now_price.toFixed(2)}` : "—"}
                                </div>
                                <Button className="addCartBtn" onClick={ () => addToCart(listing) }>
                                    Add to Cart
                                </Button>
                            </div>

                            { /* Display auction-specific details if listing is an auction */ }
                            {listing.listing_type === "auction" && (
                                <div className="bidSection">
                                    <div className="bid">
                                        {listing?.current_price ? `$${listing.current_price.toFixed(2)}` : "—"}
                                    </div>
                                    <Button className="placeBidBtn" onClick={ () => setShowAuction(true) }>
                                        Place Bid
                                    </Button>
                                    <p className="bidDescription">
                                        { listing.bids } bids. Ends: { format(new Date(listing.auction_end), "MM/dd/yyyy, hh:mm a") }
                                    </p>
                                </div>
                            )}

                            { /* Social media share buttons */ }
                            <div className="shareButtons">
                                <FacebookShareButton className="shareBtn" data-testid="facebookShareBtn" url={ location.href }>
                                    <FacebookIcon size={ 24 } round={ true } />
                                </FacebookShareButton>
                                <TwitterShareButton className="shareBtn" data-testid="twitterShareBtn" url={ location.href }>
                                    <XIcon size={ 24 } round={ true } />
                                </TwitterShareButton>
                                <PinterestShareButton className="shareBtn" data-testid="pinterestShareBtn" url={ location.href } media={ listing.image_encoded }>
                                    <PinterestIcon size={ 24 } round={ true } />
                                </PinterestShareButton>
                            </div>
                        </div>

                        { /* Display product image or fallback message */ }
                        <div className="image">
                            {listing.image_encoded ? (
                                <div style={ { position: "relative", display: "inline-block" } }>
                                    <img
                                        src={ `data:image/jpg;base64,${ listing.image_encoded  }`}
                                        alt={ listing.title }
                                        style={ { display: "block" } }
                                    />
                                    {model && (
                                        <Button
                                            className="modelBtn"
                                            onClick={ () => setShowModel(true) }
                                        >
                                            <IoMdCube className="icon" />
                                        </Button>
                                    )}
                                </div>
                            ) : (
                                <div>No image available</div>
                            )}
                        </div>

                        { /* Display product description */ }
                        <div className="description">
                            <div className="title">Description:</div>
                            {getParsedDescription() &&
                                (typeof getParsedDescription() === "string" ? (
                                    <p>{getParsedDescription()}</p>
                                ) : Array.isArray(getParsedDescription()) ? (
                                    <ul className="list">
                                        {getParsedDescription().map((desc, index) => (
                                            <li key={index}>{desc}</li>
                                        ))}
                                    </ul>
                                ) : typeof getParsedDescription() === "object" ? (
                                    <div>{JSON.stringify(getParsedDescription())}</div>
                                ) : (
                                    <div>No description available</div>
                                ))}
                        </div>
                    </div>

                    <div className="secondaryInfo">
                        { /* Additional listing information */ }
                        <div className="specifics">
                            {getParsedItemSpecifics() && (
                                typeof getParsedItemSpecifics() === "string" ? (
                                    <p>{getParsedItemSpecifics()}</p>
                                ) : Array.isArray(getParsedItemSpecifics()) ? (
                                    <ul>
                                        {getParsedItemSpecifics().map((item, index) => (
                                            <li key={index}>{item}</li>
                                        ))}
                                    </ul>
                                ) : typeof getParsedItemSpecifics() === "object" ? (
                                    <table>
                                        <caption>Item Specifics</caption>
                                        <tbody>
                                        {Object.keys(getParsedItemSpecifics()).map((key, index) => (
                                            <tr key={index}>
                                                <th>{key}</th>
                                                <td>{getParsedItemSpecifics()[key]}</td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                ) : (
                                    <div>No item specifics available</div>
                                )
                            )}
                        </div>

                        { /* Reviews section */ }
                        <div className="reviewSection">
                            {reviews &&
                                reviews.map((review, index) => (
                                    <div className="review" key={ index }>
                                        <div className="left">
                                            { renderStars(review.stars) }
                                            <p>- by { review.username }</p>
                                            <p className="date">{ dayjs.utc(review.created_at).format("YYYY-MM-DD HH:mm:ss") }</p>
                                        </div>
                                        <div className="right">
                                            <h3>{ review.title }</h3>
                                            <p>{ review.description }</p>
                                        </div>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
                {showModel && model && (
                    <>
                        <Listing3D modelPath={ model.file_reference } />
                        <Button className="closeShowcaseBtn" onClick={ () => setShowModel(false) }>
                            <ImCross size={ 24 } />
                        </Button>
                    </>
                )}
                {showAuction && (
                    <>
                        <LiveAuction listing={ listing } />
                        <Button className="closeShowcaseBtn" onClick={ () => setShowAuction(false) }>
                            <ImCross size={ 24 } />
                        </Button>
                    </>
                )}
            </div>
            { /* Right-side navigation */ }
            <RightNav />
        </div>
    );
}

export default Listing;

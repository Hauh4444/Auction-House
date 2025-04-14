// External Libraries
import { useEffect, useState } from  "react";
import { useLocation } from "react-router-dom";
import { FacebookIcon, FacebookShareButton, PinterestIcon, PinterestShareButton, TwitterShareButton, XIcon } from "react-share";
import { IoMdCube } from "react-icons/io";
import { ImCross } from "react-icons/im";
import { Button } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import Listing3D from "@/Components/Listing3D/Listing3D";
import { renderStars } from "@/utils/helpers";
import { useCart } from "@/ContextAPI/CartContext";

// Stylesheets
import "./Listing.scss";

/**
 * Listing Component
 *
 * This component fetches and displays a listing based on query parameters from the URL.
 * It utilizes React's `useEffect` and `useState` Hooks to manage the API request and state updates.
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

    /**
     * Fetches listing data based on the "key" parameter in the URL.
     * The effect runs every time `location.search` changes.
     */
    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/${ filters.key }/`,
            {
                headers: { "Content-Type": "application/json" },
            })
            .then((res) => {
                setListing(res.data.listing)
                getListingObjects(res.data.listing.listing_id)
            }) // Update state with fetched data
            .catch(err => console.error(err)); // Log errors if any
    }, [location.search]); // Call on update of URL filters

    /**
     * Fetches listing review data of the three best reviews based on the listing_id parameter.
     * The effect runs every time `location.search` changes.
     */
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

    const openModel = () => {
        setShowModel(true);

        // Add event listener for Escape key press when model is opened
        const handleEscapeKey = (event) => {
            if (event.key === "Escape") {
                closeModel(); // Close model when Escape is pressed
            }
        };

        // Add event listener to the window object
        window.addEventListener("keydown", handleEscapeKey);

        // Clean up function to remove the event listener when the model is closed
        return () => {
            window.removeEventListener("keydown", handleEscapeKey);
        };
    }

    const closeModel = () => {
        setShowModel(false);
    }

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

                            { /* Display auction-specific details if listing is an auction */ }
                            {listing.listing_type === "auction" && (
                                <>
                                    <div className="bid">${ listing.current_price }</div>
                                    <Button className="placeBidBtn">Place Bid</Button>
                                    <p className="bidDescription">{ listing.bids } bids. Ends: { listing.auction_end }</p>
                                </>
                            )}

                            { /* Display buy-now price */ }
                            <div className="price">${ listing.buy_now_price }</div>
                            <Button className="addCartBtn" onClick={ () => addToCart(listing) }>Add to Cart</Button>

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
                                <div style={ { position: 'relative', display: 'inline-block' } }>
                                    <img
                                        src={ `data:image/jpg;base64,${ listing.image_encoded  }`}
                                        alt={ listing.title }
                                        style={ { display: 'block' } } // prevents spacing under image
                                    />
                                    {/*
                                        This will be replaced with a seperate call to get the model
                                        instead of expecting the listing attribute model
                                    */}
                                    {model && (
                                        <Button
                                            className="modelBtn"
                                            onClick={ () => openModel() }
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
                            {listing.description &&
                            Array.isArray(JSON.parse(listing.description)) &&
                            JSON.parse(listing.description).length > 0 ? (
                                <ul className="list">
                                    {JSON.parse(listing.description).map((desc, index) => (
                                        <li key={ index }>{ desc }</li>
                                    ))}
                                </ul>
                            ) : (
                                <div>No description available</div>
                            )}
                        </div>
                    </div>
                    <div className="secondaryInfo">
                        { /* Additional listing information */ }
                        <div className="specifics">
                            {listing.item_specifics && (
                                // Check if item_specifics is an object (or array)
                                typeof JSON.parse(listing.item_specifics) === "object" ? (
                                    // If it's an array, display as a list
                                    Array.isArray(JSON.parse(listing.item_specifics)) ? (
                                        <ul>
                                            {JSON.parse(listing.item_specifics).map((item, index) => (
                                                <li key={ index }>{ item }</li>
                                            ))}
                                        </ul>
                                    ) : (
                                        // If it's an object, display as a table of key-value pairs
                                        <table>
                                            <caption>Item Specifics</caption>
                                            <tbody>
                                            {Object.keys(JSON.parse(listing.item_specifics)).map((key, index) => (
                                                <tr key={ index }>
                                                    <th>{ key }</th>
                                                    <td>{ JSON.parse(listing.item_specifics)[key] }</td>
                                                </tr>
                                            ))}
                                            </tbody>
                                        </table>
                                    )
                                ) : (
                                    // If it's a plain string, display it as a paragraph
                                    <p>{ listing.item_specifics }</p>
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
                                            <p className="date">{ review.created_at }</p>
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
                        <Listing3D modelPath={model.file_reference} />
                        <Button className="closeShowcaseBtn" onClick={ () => closeModel() }>
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

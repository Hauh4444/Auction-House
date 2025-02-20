// External Libraries
import { useLocation } from "react-router-dom";
import { FacebookShareButton, FacebookIcon, TwitterShareButton, XIcon, PinterestShareButton, PinterestIcon } from "react-share";
import { Button } from "@mui/material";
import PropTypes from "prop-types";

// Stylesheets
import "./Main.scss"

/**
 * Main component displays detailed information about a product listing.
 *
 * Features:
 * - Displays the product title, price, and description.
 * - If the listing is an auction, it shows the current bid price, bid count, and auction end time.
 * - Provides "Place Bid" and "Add to Cart" buttons.
 * - Includes social media share buttons for Facebook, Twitter, and Pinterest.
 * - Displays the product image if available; otherwise, a fallback message is shown.
 * - If the description is formatted as an array, it is displayed as a list.
 *
 * @param {Object} props - Component props.
 * @param {Object} props.listing - The listing object containing product details.
 * @param {string} props.listing.title - The product title.
 * @param {string} props.listing.description - The product description (JSON-formatted array or string).
 * @param {string} props.listing.listing_type - The type of listing (e.g., "auction").
 * @param {number} props.listing.current_price - The current bid price (if auction).
 * @param {number} props.listing.buy_now_price - The buy-now price.
 * @param {string} props.listing.auction_end - The auction end date/time.
 * @param {string} props.listing.image_encoded - Base64-encoded image data.
 * @param {number} props.listing.bids - The number of bids (if auction).
 *
 * @returns {JSX.Element} The rendered product details section.
 */
const Main = ({listing}) => {
    const location = useLocation();

    return (
        <div className="main">
            <div className="info">
                <div className="title">{listing.title}</div>
                {listing.listing_type === "auction" && (
                    <>
                        <div className="bid">${listing.current_price}</div>
                        <Button className="placeBidBtn">Place Bid</Button>
                        <p className="bidDescription">{listing.bids} bids. Ends: {listing.auction_end}</p>
                    < />
                )}
                <div className="price">${listing.buy_now_price}</div>
                <Button className="addCartBtn">Add to Cart</Button>
                <div className="shareButtons">
                    <FacebookShareButton
                        className="shareBtn"
                        url={location.href}
                        network="Facebook"
                    >
                        <FacebookIcon size={24} round={true} />
                    </FacebookShareButton>
                    <TwitterShareButton
                        className="shareBtn"
                        url={location.href}
                        network="Twitter"
                    >
                        <XIcon size={24} round={true} />
                    </TwitterShareButton>
                    <PinterestShareButton
                        className="shareBtn"
                        url={location.href}
                        network="Pinterest"
                        media={listing.image_encoded}
                    >
                        <PinterestIcon size={24} round={true} />
                    </PinterestShareButton>
                </div>
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
                        {JSON.parse(listing.description).map((desc, index) => (
                            <li key={index}>{desc}</li>
                        ))}
                    </ul>
                ) : (
                    <div>No description available</div>
                )}
            </div>
        </div>
    )
}

Main.propTypes = {
    listing: PropTypes.shape({
        title: PropTypes.string,
        description: PropTypes.string,
        listing_type: PropTypes.string,
        current_price: PropTypes.number,
        buy_now_price: PropTypes.number,
        auction_end: PropTypes.string,
        image_encoded: PropTypes.string,
        bids: PropTypes.number,
    }),
};

export default Main;
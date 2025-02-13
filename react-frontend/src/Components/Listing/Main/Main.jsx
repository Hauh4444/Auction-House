// External Libraries
import {Button} from "@mui/material";
import PropTypes from "prop-types";
// Stylesheets
import "./Main.scss"

const Main = ({listing}) => {

    return (
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
                    <img src={"data:image/jpg;base64," + listing.image_encoded} alt={listing.title}/>
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
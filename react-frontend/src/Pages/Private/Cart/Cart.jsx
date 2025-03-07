// External Libraries
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiPlus, FiMinus } from "react-icons/fi";
import { BsTrash3Fill } from "react-icons/bs";
import { Button } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { renderStars, navigateToListing } from "@/utils/helpers";
import { useCart } from "@/ContextAPI/CartContext"

// Stylesheets
import "./Cart.scss";

const Cart = () => {
    const navigate = useNavigate(); // Navigate hook for routing

    const { addToCart, removeFromCart } = useCart(); // Access authentication functions from the AuthProvider context

    const [cartItems, setCartItems] = useState([]);

    // Fetch cart items from localStorage when component mounts
    useEffect(() => {
        getCartItems();
    }, []);

    const getCartItems = () => {
        const items = JSON.parse(localStorage.getItem("cartItems")) || [];
        setCartItems(items);
    }

    const removeItem = async (item) => {
        await removeFromCart(item);
        getCartItems();
    }

    const addItem = async (item) => {
        await addToCart(item);
        getCartItems();
    }

    return (
        <div className="cartPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                {/* Loop through cartItems and display each one */}
                <div className="cartListings">
                    {cartItems.length > 0 ? (
                        cartItems.map((item, index) => (
                            <div className="cartItem" key={index}>
                                <div className="itemImage">
                                    {/* Display the product image */}
                                    <img src={`data:image/jpg;base64,${item.image_encoded}`} alt="" />
                                </div>
                                <div className="itemContent">
                                    {/* Button to navigate to the detailed listing view */}
                                    <Button className="itemHead" onClick={() => navigateToListing(item.listing_id, navigate)}>
                                        {item.title_short}
                                    </Button>
                                    <div className="review">
                                        {/* Render the star rating based on the average review */}
                                        {renderStars(item.average_review)}
                                        {/* Display the total number of reviews */}
                                        <span className="totalReviews" style={{left: -16 * Math.ceil(item.average_review) + "px"}}>
                                            &emsp;{item.total_reviews}
                                        </span>
                                    </div>
                                    <h2 className="itemPrice">
                                        ${item.buy_now_price} {/* Display the product price */}
                                    </h2>
                                    <div className="itemQuantity">
                                        <Button className="quantityDown" onClick={() => removeItem(item)}>
                                            {item.quantity > 1 ? (
                                                <FiMinus className="icon" />
                                            ) : (
                                                <BsTrash3Fill className="icon" />
                                            )}
                                        </Button>
                                        <div className="quantity">
                                            {item.quantity}
                                        </div>
                                        <Button className="quantityUp" onClick={() => addItem(item)}>
                                            <FiPlus className="icon" />
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>Your cart is empty</p>
                    )}
                </div>
            </div>

            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default Cart;

// External Libraries
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiPlus, FiMinus } from "react-icons/fi";
import { BsTrash3Fill } from "react-icons/bs";
import { Button } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { renderStars, navigateToListing } from "@/utils/helpers";
import { useCart } from "@/ContextAPI/CartContext"

// Stylesheets
import "./Cart.scss";

const Cart = () => {
    const navigate = useNavigate(); // Navigate hook for routing

    const { addToCart, removeFromCart, clearCart, getCartTotal } = useCart(); // Access authentication functions from the AuthProvider context

    const [cartItems, setCartItems] = useState([]);

    useEffect(() => {
        getCartItems();
    }, []);

    const getCartItems = () => {
        const items = JSON.parse(localStorage.getItem("cartItems")) || [];
        setCartItems(items);
    }

    const getTotalItems = () => {
        return cartItems.reduce((total, item) => total + item.quantity, 0);
    }

    const purchaseCart = async () => {
        if (!cartItems.length) {
            return;
        }
        axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/purchase/`,
            {
                listings: cartItems,
                total_amount: getCartTotal(),
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true, // Ensure cookies are sent
            })
            .then(async () => {
                await clearCart();
                setCartItems([]);
            })
            .catch(err => console.log(err)); // Log errors if any
    }

    return (
        <div className="cartPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                {/* Loop through cartItems and display each one */}
                <div className="cart">
                    <div className="cartHead">
                        <h3 style={{ flexBasis: "calc(40% + 140px)" }}>Info</h3>
                        <h3 style={{ flexBasis: "calc(20% - 40px)" }}>Price</h3>
                        <h3 style={{ flexBasis: "calc(20% - 40px)" }}>Quantity</h3>
                        <h3 style={{ flexBasis: "calc(20% - 40px)" }}>Total Price</h3>
                    </div>
                    {cartItems.length > 0 ? (
                        cartItems.map((item, index) => (
                            <div className="cartItem" key={index}>
                                <div className="itemImage">
                                    {/* Display the product image */}
                                    <img src={`data:image/jpg;base64,${item.image_encoded}`} alt="" />
                                </div>
                                <div className="itemContent">
                                    <div className="basicInfo">
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
                                    </div>
                                    <h2 className="itemPrice">
                                        ${item.buy_now_price} {/* Display the product price */}
                                    </h2>
                                    <div className="itemQuantity">
                                        <div className="btns">
                                            <Button className="quantityDown" onClick={async () => {
                                                await removeFromCart(item);
                                                getCartItems();
                                            }}>
                                                {item.quantity > 1 ? (
                                                    <FiMinus className="icon" />
                                                ) : (
                                                    <BsTrash3Fill className="icon" />
                                                )}
                                            </Button>
                                            <div className="quantity">
                                                {item.quantity}
                                            </div>
                                            <Button className="quantityUp" onClick={async () => {
                                                await addToCart(item);
                                                getCartItems();
                                            }}>
                                                <FiPlus className="icon" />
                                            </Button>
                                        </div>
                                    </div>
                                    <h2 className="totalItemPrice">
                                        ${(cartItems[index].buy_now_price * cartItems[index].quantity).toFixed(2)}
                                    </h2>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>Your cart is empty</p>
                    )}
                    <div className="checkout">
                        <h2 className="subtotal">Subtotal {getTotalItems()} {getTotalItems() > 1 ? "Items" : "Item"}: <b>${getCartTotal()}</b></h2>
                        <Button className="btn" onClick={() => purchaseCart()}>
                            Proceed To Checkout
                        </Button>
                    </div>
                </div>
            </div>

            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default Cart;

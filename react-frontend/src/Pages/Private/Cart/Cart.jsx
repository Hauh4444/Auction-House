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

    useEffect(() => {
        getCartItems();
    }, []);

    const getCartItems = () => {
        const items = JSON.parse(localStorage.getItem("cartItems")) || [];
        setCartItems(items);
    }

    const getTotalCartItems = () => {
        return cartItems.reduce((total, item) => total + item.quantity, 0);

    }

    const getTotalPrice = () => {
        return cartItems.reduce((total, item) => total + item.buy_now_price * item.quantity, 0).toFixed(2);
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
                        <h2 className="subtotal">Subtotal {getTotalCartItems()} {getTotalCartItems() > 1 ? "Items" : "Item"}: <b>${getTotalPrice()}</b></h2>
                        <Button className="btn">
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

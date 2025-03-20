// External Libraries
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, MenuItem, Select } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import { renderStars, navigateToListing, updateList } from "@/utils/helpers";
import { useCart } from "@/ContextAPI/CartContext";

// Stylesheets
import "./Lists.scss";

const Lists = () => {
    const navigate = useNavigate(); // Navigate hook for routing

    const { addToCart } = useCart(); // Access authentication functions from the AuthProvider context

    const [lists, setLists] = useState([]);
    const [list, setList] = useState(null);
    const [listItems, setListItems] = useState([]);

    // Fetch user list data from the backend API
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/user/lists/", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensures cookies are sent with requests
        })
            .then(res => {
                setLists(res.data.lists);
                goToList(res.data.lists[0]);
            }) // Set the lists state
            .catch(() => setLists([]));
    }, []);

    const goToList = (list) => {
        setList(list);

        axios.get(`http://127.0.0.1:5000/api/user/lists/${list.list_id}/`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
            .then(res => setListItems(res.data.list_items))
            .catch(() => setListItems([]));
    }

    const removeFromList = (index) => {
        const updatedItems = [...listItems];
        updatedItems.splice(index, 1);
        setListItems(updatedItems);
        updateList(list.list_id, updatedItems);
    }

    return (
        <div className="userListsPage page" data-testid="userListsPage">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <div className="listListings">
                    {lists && list && (
                        <div className="listHead">
                            <Select
                                className="listsInput"
                                value={list.list_id}
                                label="List"
                                onChange={(e) => goToList(lists.find(l => l.list_id === e.target.value))}
                                sx={{
                                    backgroundColor: "transparent",
                                    "& .MuiSelect-select": {
                                        display: "flex",
                                        alignItems: "center",
                                        paddingTop: "0",
                                        paddingBottom: "0",
                                    },
                                    "&:before, &:after": { display: "none" },
                                }}
                                variant="filled"
                            >
                                {lists.map((list, index) => (
                                    <MenuItem value={list.list_id} key={index}>{list.title}</MenuItem>
                                ))}
                            </Select>
                        </div>
                    )}
                    {listItems ? (
                        listItems.map((listing, index) => (
                            <div
                                className="listing"
                                key={index}
                            >
                                <div className="image">
                                    {/* Display the product image */}
                                    <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                                </div>
                                <div className="info">
                                    {/* Button to navigate to the detailed listing view */}
                                    <Button className="title" onClick={() => navigateToListing(listing.listing_id, navigate)}>
                                        {listing.title}
                                    </Button>
                                    <div className="review">
                                        {/* Render the star rating based on the average review */}
                                        {renderStars(listing.average_review)}
                                        {/* Display the total number of reviews */}
                                        <span className="totalReviews" style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                    &emsp;{listing.total_reviews}
                                </span>
                                    </div>
                                    <h2 className="price">
                                        ${listing.buy_now_price} {/* Display the product price */}
                                    </h2>
                                </div>
                                <div className="btns">
                                    <Button className="removeFromListBtn" onClick={() => removeFromList(index)}>Remove</Button>
                                    {/* Button to add the product to the cart */}
                                    <Button className="addCartBtn" onClick={() => addToCart(listing)}>Add to Cart</Button>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>Your list is empty</p>
                    )}
                </div>
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    )
}

export default Lists;
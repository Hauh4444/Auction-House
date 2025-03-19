// External Libraries
import { useEffect, useState } from "react";
import {useLocation, useNavigate} from "react-router-dom";
import { Button, Card, CardContent, FormControl, InputLabel, Select, MenuItem, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import SellerProfileNav from "@/Components/Navigation/SellerProfileNav/SellerProfileNav";
import { useAuth } from "@/ContextAPI/AuthContext";
import { renderStars, navigateToListing, encodeImageToBase64 } from "@/utils/helpers";

// Stylesheets
import "./SellerProfile.scss";

const SellerProfile = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from the URL
    const auth = useAuth(); // Access authentication functions from the AuthProvider context

    const [listings, setListings] = useState([]);

    const [listing, setListing] = useState({
        image_encoded: "",
        title: "",
        title_short: "",
        description: "",
        item_specifics: "",
        category_id: "",
        listing_type: "buy_now",
        starting_price: 0,
        reserve_price: 0,
        auction_end: "",
        buy_now_price: 0,
    }) // State to hold uploaded listing data
    const [categories, setCategories] = useState([]); // State to hold category data
    const [listingCategory, setListingCategory] = useState("") // State to hold currently selected category data
    const tempImage = useState("") // State to hold blank encoded image

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/user/" + auth.user + "/listings", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => setListings(res.data.listings))
            .catch(err => console.log(err)); // Log errors if any
    }, []);

    useEffect(() => {
        // Fetch categories from the backend API when the component mounts
        axios.get("http://127.0.0.1:5000/api/categories", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => setCategories(res.data.categories)) // Update state with fetched data
            .catch(err => console.log(err)); // Log errors if any
    }, []); // Empty dependency array ensures this effect runs only once

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            encodeImageToBase64(file)
                .then((base64String) => {
                    const image_encoded = `data:image/jpg;base64,${base64String}`;
                    setListing({ ...listing, image_encoded: image_encoded }); // Save the file object for upload
                })
                .catch((error) => console.error("Error encoding image:", error)); // Log errors if any
        }
    };

    // On submit, post new listing to the backend API
    const handleSubmit = () => {
        console.log(listing)
        axios.post("http://127.0.0.1:5000/api/listings/",
            {
                listing: listing,
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true, // Ensure cookies are sent
            })
            .then(() => navigate("/"))
            .catch(err => console.log(err)); // Log errors if any
    }

    return (
        <div className="sellerProfilePage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <SellerProfileNav />

                {filters.nav === "manage" ? (
                    <div className="listings">
                        {listings.map((listing, index) => (
                            <div className="listing" key={index}>
                                <div className="image">
                                    <img src={`data:image/jpg;base64,${listing.image_encoded}`} alt="" />
                                </div>
                                <div className="info">
                                    <div className="review">
                                        {renderStars(listing.average_review)} {/* Render the star ratings */}
                                        <span className="totalReviews"
                                              style={{left: -16 * Math.ceil(listing.average_review) + "px"}}>
                                                    &emsp;{listing.total_reviews} {/* Display the total reviews */}
                                                </span>
                                    </div>
                                    <Button
                                        className="title"
                                        onClick={() => navigateToListing(listing.listing_id, navigate)}
                                    >
                                        {listing.title_short} {/* Display the listing title */}
                                    </Button>
                                    <h2 className="price">${listing.buy_now_price}</h2> {/* Display the price */}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <Card className="productUploadCard">
                        <CardContent className="content">
                            <div className="imageUpload">
                                <img
                                    src={ `data:image/jpg;base64,${listing.image_encoded || `data:image/jpg;base64,${tempImage}`}` }
                                    alt="Product Image"
                                    className="product-image"
                                />
                                <input
                                    type="file"
                                    accept="image/*"
                                    className="product-picture"
                                    style={{ display: "none" }}
                                    onChange={ handleImageChange }
                                />
                                <Button
                                    className="btn"
                                    component="label"
                                    htmlFor="product-picture"
                                >
                                    Choose File
                                </Button>
                            </div>
                            <TextField
                                className="input"
                                label="Title"
                                name="title"
                                type="text"
                                variant="outlined"
                                value={listing.title}
                                onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                required
                            />
                            <TextField
                                className="input"
                                label="Title Short"
                                name="title_short"
                                type="text"
                                variant="outlined"
                                value={listing.title_short}
                                onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                slotProps={{ htmlInput: { maxLength: 20 } }}
                                required
                            />
                            <TextField
                                className="input"
                                label="Description"
                                name="description"
                                type="text"
                                variant="outlined"
                                value={listing.description}
                                onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                required
                                multiline={true}
                                rows={5}
                                maxrows={10}
                                fullWidth={true}
                            />
                            <TextField
                                className="input"
                                label="Item Specifics"
                                name="item_specifics"
                                type="text"
                                variant="outlined"
                                value={listing.item_specifics}
                                onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                required
                                multiline={true}
                                rows={5}
                                maxrows={10}
                                fullWidth={true}
                            />
                            <FormControl>
                                <InputLabel className="categorySelectLabel">Category</InputLabel>
                                <Select
                                    className="categorySelect"
                                    labelId="categorySelectLabel"
                                    name="category_id"
                                    variant="outlined"
                                    value={listingCategory}
                                    onChange={(e) => {
                                        setListingCategory(e.target.value);
                                        setListing({ ...listing, [e.target.name]: e.target.value });
                                    }}
                                >
                                    {categories.map((category, index) => (
                                        <MenuItem value={category.category_id} key={index}>{category.name}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <FormControl>
                                <InputLabel className="listingTypeLabel">Listing Type</InputLabel>
                                <Select
                                    className="listingType"
                                    labelId="listingTypeLabel"
                                    name="listing_type"
                                    variant="outlined"
                                    value={listing.listing_type}
                                    onChange={(e) => {
                                        setListing({ ...listing, [e.target.name]: e.target.value });
                                    }}
                                >
                                    <MenuItem value="auction">Auction</MenuItem>
                                    <MenuItem value="buy_now">Purchase</MenuItem>
                                </Select>
                            </FormControl>
                            { listing.listing_type === "auction" && (
                                <>
                                    <TextField
                                        className="input"
                                        label="Starting Price"
                                        name="starting_price"
                                        type="number"
                                        variant="outlined"
                                        value={listing.starting_price}
                                        onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                        required
                                    />
                                    <TextField
                                        className="input"
                                        label="Reserve Price"
                                        name="reserve_price"
                                        type="number"
                                        variant="outlined"
                                        value={listing.reserve_price}
                                        onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                        required
                                    />
                                    <TextField
                                        className="input"
                                        label="Auction End"
                                        name="auction_end"
                                        type="date"
                                        variant="outlined"
                                        value={listing.auction_end}
                                        onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                        required
                                    />
                                </>
                            )}
                            <TextField
                                className="input"
                                label="Buy Now Price"
                                name="buy_now_price"
                                type="number"
                                variant="outlined"
                                value={listing.buy_now_price}
                                onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                                required
                            />
                            {/* Submit button */}
                            <Button className="btn" onClick={() => handleSubmit(listing)}>Submit</Button>
                        </CardContent>
                    </Card>
                )}
            </div>
            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
}

export default SellerProfile;
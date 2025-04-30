// External Libraries
import {useEffect, useRef, useState} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Card, CardContent, FormControl, InputLabel, Select, MenuItem, TextField } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import SellerProfileNav from "@/Components/Navigation/SellerProfileNav/SellerProfileNav";
import { renderStars, navigateToListing, encodeImageToBase64 } from "@/utils/helpers";
import tempImage from "@/assets/images/noImage.webp"

// Stylesheets
import "./SellerProfile.scss";

const SellerProfile = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from the URL

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
        auction_end: null,
        buy_now_price: 0
    }) // State to hold uploaded listing data
    const [categories, setCategories] = useState([]); // State to hold category data
    const [listingCategory, setListingCategory] = useState("") // State to hold currently selected category data

    const smallInputRef = useRef(null);
    const imgRef = useRef(null);

    useEffect(() => {
        async function encode() {
            const response = await fetch(tempImage);
            const blob = await response.blob();
            const base64 = await encodeImageToBase64(blob);
            setListing({ ...listing, image_encoded: base64 });
        }
        encode();
    }, []);

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/listings/`,
            {
                headers: { "Content-Type": "application/json" },
            })
            .then((res) => setListings(res.data.listings))
            .catch((err) => console.error(err)); // Log errors if any
    }, []);

    useEffect(() => {
        // Fetch categories from the backend API when the component mounts
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/categories/`,
            {
                headers: { "Content-Type": "application/json" },
            })
            .then((res) => setCategories(res.data.categories)) // Update state with fetched data
            .catch((err) => console.error(err)); // Log errors if any
    }, []); // Empty dependency array ensures this effect runs only once

    const handleImageChange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            console.log("Selected file:", file);
            const base64Image = await encodeImageToBase64(file);
            console.log("Base64 Image:", base64Image);
            setListing({ ...listing, image_encoded: base64Image });
        }
    };

    useEffect(() => {
        if (filters.nav === "upload") {
            let height = smallInputRef.current.offsetHeight;
            imgRef.current.style.maxHeight = height + "px";
        }
    }, [listing.listing_type, filters.nav])

    const handleListingTypeChange = (e) => {
        setListing({
            ...listing,
            [e.target.name]: e.target.value,
            ...(e.target.value === "buy_now" && {
                starting_price: null,
                reserve_price: null,
                auction_end: null,
            }),
        });
    }

    // On submit, post new listing to the backend API
    const handleSubmit = () => {
        const sanitizedListing = {
            ...listing,
            starting_price: parseFloat(listing.starting_price) || 0,
            reserve_price: parseFloat(listing.reserve_price) || 0,
            buy_now_price: parseFloat(listing.buy_now_price) || 0,
            auction_end: listing.auction_end ? dayjs.utc(listing.auction_end).format("YYYY-MM-DD HH:mm:ss") : null,
        };

        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/listings/`,
            {
                listing: sanitizedListing,
            },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensure cookies are sent
            })
            .then(() => navigate("/user/seller-profile?nav=manage"))
            .catch((err) => console.error(err)); // Log errors if any
    }

    return (
        <div className="sellerProfilePage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <SellerProfileNav />

                {filters.nav === "manage" ? (
                    <div className="listings">
                        {listings.map((listing, index) => (
                            <div className="listing" key={ index }>
                                <div className="image">
                                    <img src={ `data:image/jpg;base64,${ listing.image_encoded  }`} alt="" />
                                </div>
                                <div className="info">
                                    <div className="review">
                                        { renderStars(listing.average_review) } { /* Render the star ratings */ }
                                        <span className="totalReviews"
                                              style={ { left: -16 * Math.ceil(listing.average_review) + "px" } }>
                                                    &emsp;{ listing.total_reviews } { /* Display the total reviews */ }
                                                </span>
                                    </div>
                                    <Button
                                        className="title"
                                        onClick={ () => navigateToListing(listing.listing_id, navigate) }
                                    >
                                        { listing.title_short } { /* Display the listing title */ }
                                    </Button>
                                    <h2 className="price">${ listing.buy_now_price }</h2> { /* Display the price */ }
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <Card className="productUploadCard">
                        <CardContent className="content">
                            <div className="imageUpload" ref={ imgRef }>
                                <div className="image">
                                    <img
                                        src={ `data:image/jpg;base64,${ listing.image_encoded }` }
                                        alt="Product Image"
                                        className="product-image"
                                    />
                                </div>
                                <input
                                    type="file"
                                    accept="image/*"
                                    id="product-picture"
                                    style={ { display: "none" } }
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
                            <div className="small" ref={ smallInputRef }>
                                <TextField
                                    className="input"
                                    label="Title"
                                    name="title"
                                    type="text"
                                    variant="outlined"
                                    value={ listing.title }
                                    onChange={ (e) => setListing({ ...listing, [e.target.name]: e.target.value  })}
                                    required
                                />
                                <TextField
                                    className="input"
                                    label="Title Short"
                                    name="title_short"
                                    type="text"
                                    variant="outlined"
                                    value={ listing.title_short }
                                    onChange={ (e) => setListing({ ...listing, [e.target.name]: e.target.value  })}
                                    slotProps={ { htmlInput: { maxLength: 20  } } }
                                    required
                                />
                                <FormControl className="select">
                                    <InputLabel className="categorySelectLabel">Category</InputLabel>
                                    <Select
                                        className="categorySelect"
                                        labelId="categorySelectLabel"
                                        label="Category"
                                        name="category_id"
                                        variant="outlined"
                                        value={ listingCategory }
                                        onChange={(e) => {
                                            setListingCategory(e.target.value);
                                            setListing({ ...listing, [e.target.name]: e.target.value });
                                        }}
                                    >
                                        {categories.map((category, index) => (
                                            <MenuItem value={ category.category_id } key={ index }>{ category.name }</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <FormControl className="select">
                                    <InputLabel className="listingTypeLabel">Listing Type</InputLabel>
                                    <Select
                                        className="listingType"
                                        labelId="listingTypeLabel"
                                        label="Listing Type"
                                        name="listing_type"
                                        variant="outlined"
                                        value={ listing.listing_type }
                                        onChange={ (e) => handleListingTypeChange(e) }
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
                                            value={ listing.starting_price }
                                            onChange={ (e) => setListing({ ...listing, [e.target.name]: parseFloat(e.target.value) })}  // Ensure it's a number
                                            required
                                        />
                                        <TextField
                                            className="input"
                                            label="Reserve Price"
                                            name="reserve_price"
                                            type="number"
                                            variant="outlined"
                                            value={ listing.reserve_price }
                                            onChange={ (e) => setListing({ ...listing, [e.target.name]: parseFloat(e.target.value) })}  // Ensure it's a number
                                            required
                                        />
                                        <LocalizationProvider dateAdapter={ AdapterDayjs }>
                                            <DatePicker
                                                className="input"
                                                label="Auction End"
                                                name="auction_end"
                                                value={ dayjs.utc(listing.auction_end) }
                                                onChange={ (value) => setListing({ ...listing, auction_end: value })}
                                                minDate={ dayjs().add(1, 'day') }
                                                slotProps={ { textField: { variant: "outlined" } } }
                                                required
                                            />
                                        </LocalizationProvider>
                                    </>
                                )}
                                <TextField
                                    className="input"
                                    label="Buy Now Price"
                                    name="buy_now_price"
                                    type="number"
                                    variant="outlined"
                                    value={ listing.buy_now_price }
                                    onChange={ (e) => setListing({ ...listing, [e.target.name]: parseFloat(e.target.value)  })}
                                    required
                                />
                            </div>
                            <div className="large">
                                <TextField
                                    className="input long"
                                    label="Description"
                                    name="description"
                                    type="text"
                                    variant="outlined"
                                    value={ listing.description }
                                    onChange={ (e) => setListing({ ...listing, [e.target.name]: e.target.value  })}
                                    required
                                    multiline={ true }
                                    rows={ 5 }
                                    maxrows={ 10 }
                                    fullWidth={ true }
                                />
                                <TextField
                                    className="input long"
                                    label="Item Specifics"
                                    name="item_specifics"
                                    type="text"
                                    variant="outlined"
                                    value={ listing.item_specifics }
                                    onChange={ (e) => setListing({ ...listing, [e.target.name]: e.target.value  })}
                                    required
                                    multiline={ true }
                                    rows={ 5 }
                                    maxrows={ 10 }
                                    fullWidth={ true }
                                />
                            </div>
                            { /* Submit button */ }
                            <Button className="btn" onClick={ () => handleSubmit(listing) }>Submit</Button>
                        </CardContent>
                    </Card>
                )}
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
}

export default SellerProfile;
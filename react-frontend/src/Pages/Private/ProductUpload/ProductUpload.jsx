// External Libraries
import {useEffect, useState} from "react";
import { Button, Card, CardContent, CardHeader, FormControl, InputLabel, Select, MenuItem, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./ProductUpload.scss"

const ProductUpload = () => {
    const [listing, setListing] = useState({}) // State to hold profile data
    const [categories, setCategories] = useState([]);
    const [listingCategory, setListingCategory] = useState("")
    const tempImage = useState("")

    useEffect(() => {
        // Fetch categories from the backend API when the component mounts
        axios.get("http://127.0.0.1:5000/api/categories", {
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then(res => {
                // Update state with the fetched categories
                setCategories(res.data.categories);
            })
            .catch(err => {
                // Log any errors that occur during the request
                console.log(err);
            });
    }, []); // Empty dependency array ensures this effect runs only once

    const encodeImageToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onloadend = () => {
                // The result is the base64 encoded string
                const base64String = reader.result.split(',')[1]; // Remove data URL prefix
                resolve(base64String);
            };

            reader.onerror = (error) => {
                reject(error);
            };

            reader.readAsDataURL(file); // This converts the file into a base64 string
        });
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            encodeImageToBase64(file)
                .then((base64String) => {
                    const image_encoded = `data:image/jpg;base64,${base64String}`;
                    setListing({ ...listing, image_encoded: image_encoded });
                })
                .catch((error) => {
                    console.error('Error encoding image:', error);
                });
        }
    };

    // On submit, post new listing to the backend API
    const handleSubmit = () => {
        console.log(listing);
        axios.post("http://127.0.0.1:5000/api/listings/", {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true, // Ensure cookies are sent if needed
            data: listing,
        })
            .catch(err => console.log(err)); // Log errors if any
    }

    return (
        <div className="productUploadPage page">
            <div className="mainPage">
                <Header />

                <Card className="productUploadCard">
                    <CardHeader title="Product Upload"></CardHeader>
                    <CardContent className="content">
                        <div className="imageUpload">
                            <img
                                src={`data:image/jpg;base64,${listing.image_encoded || `data:image/jpg;base64,${tempImage}`}`}
                                alt="Profile"
                                className="profile-image"
                            />
                            <input
                                type="file"
                                accept="image/*"
                                className="profile-picture"
                                style={{ display: "none" }}
                                onChange={handleImageChange}
                            />
                            <Button
                                className="btn"
                                component="label"
                                htmlFor="profile-picture"
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
                            fullWclassNameth={true}
                        />
                        <TextField
                            className="input"
                            label="Title Short"
                            name="titleShort"
                            type="text"
                            variant="outlined"
                            value={listing.title_short}
                            onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                            required
                            fullWclassNameth={true}
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
                            fullWclassNameth={true}
                        />
                        <TextField
                            className="input"
                            label="Item Specifics"
                            name="itemSpecifics"
                            type="text"
                            variant="outlined"
                            value={listing.item_specifics}
                            onChange={(e) => setListing({ ...listing, [e.target.name]: e.target.value })}
                            required
                            multiline={true}
                            rows={5}
                            maxrows={10}
                            fullWclassNameth={true}
                        />
                        <FormControl fullWclassNameth>
                            <InputLabel className="categorySelectLabel">Category</InputLabel>
                            <Select
                                labelId="categorySelectLabel"
                                className="categorySelect"
                                name="category_className"
                                value={listingCategory}
                                label="Category"
                                variant="outlined"
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
                        <FormControl fullWclassNameth>
                            <InputLabel className="listingTypeLabel">Listing Type</InputLabel>
                            <Select
                                labelId="listingTypeLabel"
                                className="listingType"
                                name="listing_type"
                                value={listing.listing_type}
                                label="Category"
                                variant="outlined"
                                onChange={(e) => {
                                    setListing({ ...listing, [e.target.name]: e.target.value });
                                }}
                            >
                                <MenuItem value="auction">Auction</MenuItem>
                                <MenuItem value="buy_now">Purchase</MenuItem>
                            </Select>
                        </FormControl>
                        {/* Submit button */}
                        <Button className="btn" onClick={() => handleSubmit(listing)}>Submit</Button>
                    </CardContent>
                </Card>
            </div>
            <RightNav />
        </div>
    );
}

export default ProductUpload;
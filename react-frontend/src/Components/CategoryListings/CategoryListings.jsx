// External Libraries
import { useState, useEffect } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import { LiaStarSolid, LiaStarHalfSolid } from "react-icons/lia";
import { MdArrowBackIosNew, MdArrowForwardIos } from "react-icons/md";
import { Button } from "@mui/material";
import axios from "axios";
// Stylesheets
import "./CategoryListings.scss";

const SearchListings = () => {
    const [listings, setListings] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries());

    useEffect(() => {

        filters.sort = filters.nav === "new" ? "created_at" : (filters.nav === "best-sellers" ? "purchases" : filters.sort);
        filters.order = filters.nav === "new" || filters.nav === "best-sellers" ? "desc" : filters.order;

        axios.get("http://127.0.0.1:5000/api/listings", {
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                query: filters.query,
                category: filters.category,
                sort: filters.sort,
                order: filters.order,
                start: 1,
                end: 20,
            }
        })
            .then(res => setListings(res.data))
            .catch(err => console.log(err));
    }, [location.search]);

    function navigateToListing(id) {
        navigate({
            pathname: "/listings",
            search: createSearchParams({
                key: id
            }).toString(),
        });
    }

    // Function to handle pagination
    function pagination(n) {
        // Increment or decrement the page number (p) in filters
        filters.page = parseInt(filters.page) + n;
        // Update the URL with the new filters (this causes a re-render)
        navigate({
            pathname: "/category",
            search: createSearchParams(filters).toString(), // Convert filters object to query string
        });
        let obj = document.querySelector(".categoryListingsHead");
        let objTop = 0;
        if (obj.offsetParent) {
            do {
                objTop += obj.offsetTop;
            } while ((obj = obj.offsetParent));
        }
        window.scrollTo(0, objTop - 50);
    }

    return (
        <>
            <h1 className="categoryListingsHead">View All</h1>
            <div className="categoryListings">
                {listings.map((listing, index) => (
                    <div className={`listing ${index % 4 === 0 ? "first" : ""}`} key={index}>
                        <div className="listingImage">
                            <img src={"data:image/jpg;base64," + listing.image_encoded} alt="" />
                        </div>
                        <div className="listingInfo">
                            <div className="listingReviews">
                                {Array.from({ length: 5 }, (_, i) => (
                                    <LiaStarSolid className="blankStar" key={i} />
                                ))}
                                {Array.from({ length: listing.average_review }, (_, i) => (
                                    <LiaStarSolid className="filledStar" key={i} />
                                ))}
                                {listing.average_review > Math.floor(listing.average_review) && (
                                    <LiaStarHalfSolid className="halfStar" />
                                )}
                                <span
                                    className={"reviews"}
                                    style={{ left: -16 * Math.ceil(listing.average_review) + "px" }}
                                >
                                    &emsp;{listing.total_reviews}
                                </span>
                            </div>
                            <Button className="listingTitle" onClick={() => navigateToListing(listing.listing_id)}>
                                {listing.title_short}
                            </Button>
                            <h2 className="listingPrice">${listing.buy_now_price}</h2>
                        </div>
                    </div>
                ))}
            </div>
            <div className="pagination">
                <Button onClick={() => pagination(-1)}><MdArrowBackIosNew className="icon" />&ensp;Previous</Button>
                <Button style={{ marginLeft: "25px" }} onClick={() => pagination(1)}>Next&ensp;<MdArrowForwardIos className="icon" /></Button>
            </div>
        </>
    );
};

export default SearchListings;

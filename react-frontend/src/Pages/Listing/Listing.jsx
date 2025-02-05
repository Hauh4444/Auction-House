import SearchBar from "@//Components/SearchBar/SearchBar";
import LeftNavigation from "@//Components/LeftNavigation/LeftNavigation";
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import "./Listing.scss";

const Listing = () => {
    const [listing, setListing] = useState({});
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/listings/" + queryParams.get("key"), {
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => {
                setListing(res.data.listing);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    return (

        <div className="searchPage">
            <div style={{height: "100%", display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "70%"}}>
                    <SearchBar />
                    <div className="mainPage">
                        <div className="headNav">

                        </div>
                        <div className="listing">
                            <div className="listingImage">
                                <img src={"data:image/jpg;base64," + listing.image} alt="" />
                            </div>
                            <div className="listingDescription">
                                <div className="listingTitle">
                                    {listing.title}
                                </div>
                                <h1 className="listingPrice">
                                    ${listing.price}
                                </h1>
                            </div>
                        </div>
                    </div>
                </div>
                <RightNavigation />
            </div>
        </div>
    )
}

export default Listing;
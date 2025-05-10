// External Libraries
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import SellerProfileNav from "@/Components/Navigation/SellerProfileNav/SellerProfileNav";
import ProductManage from "@/Components/ProductManage/ProductManage.jsx";
import { renderStars } from "@/utils/helpers";

// Stylesheets
import "./SellerProfile.scss";

const SellerProfile = () => {
    const navigate = useNavigate(); // Navigate hook for routing
    const location = useLocation(); // Hook to access the current location (URL)
    const filters = Object.fromEntries(new URLSearchParams(location.search).entries()); // Extract query parameters from the URL

    const [listings, setListings] = useState([]);

    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/listings/`,
            {
                headers: { "Content-Type": "application/json" },
            })
            .then((res) => setListings(res.data.listings))
            .catch((err) => console.error(err)); // Log errors if any
    }, []);

    return (
        <div className="sellerProfilePage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <SellerProfileNav />

                {filters.nav === "manage" ? (
                    <div className="listings">
                        {listings.map((item, index) => (
                            <div className="listing" key={ index }>
                                <div className="image">
                                    <img src={ `data:image/jpg;base64,${ item.image_encoded  }`} alt="" />
                                </div>
                                <div className="info">
                                    <div className="review">
                                        { renderStars(item.average_review) } { /* Render the star ratings */ }
                                        <span className="totalReviews"
                                              style={ { left: -16 * Math.ceil(item.average_review) + "px" } }>
                                                    &emsp;{ item.total_reviews } { /* Display the total reviews */ }
                                                </span>
                                    </div>
                                    <Button
                                        className="title"
                                        onClick={ () => navigate(`/user/listings/${ item.listing_id }`) }
                                    >
                                        { item.title_short } { /* Display the listing title */ }
                                    </Button>
                                    <h2 className="price">${ item.buy_now_price }</h2> { /* Display the price */ }
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <ProductManage httpType="post" />
                )}
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
}

export default SellerProfile;
// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";
import ProductManage from "@/Components/ProductManage/ProductManage.jsx";

// Stylesheets
import "./ManageListing.scss";

const ManageListing = () => {

    return (
        <div className="manageListingPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <h1>Manage Listing</h1>

                <div className="card">
                    <ProductManage httpType="put" />
                </div>
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    );
}

export default ManageListing;
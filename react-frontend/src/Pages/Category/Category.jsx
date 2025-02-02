import SearchBar from '../../Components/SearchBar/SearchBar';
import LeftNavigation from "../../Components/LeftNavigation/LeftNavigation";
import RightNavigation from "../../Components/RightNavigation/RightNavigation.jsx";
import Listings from "../../Components/Listings/Listings";
import './Category.scss';

const Category = () => {
    return (
        <div className="categoryPage">
            <div style={{display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "50%"}}>
                    <SearchBar />
                    <Listings />
                </div>
                <RightNavigation />
            </div>
        </div>
    )
}

export default Category;
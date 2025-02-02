import Header from '../../Components/Header/Header';
import Listings from '../../Components/Listings/Listings';
import LeftNavigation from "../../Components/LeftNavigation/LeftNavigation.jsx";
import RightNavigation from "../../Components/RightNavigation/RightNavigation.jsx";
import SearchBar from "../../Components/SearchBar/SearchBar.jsx";
import './Search.scss';

const Search = () => {
    return (
        <div className="searchPage">
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

export default Search;
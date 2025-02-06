import Header from "@/Components/Header/Header";
import SearchNavigation from "@/Components/SearchNavigation/SearchNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import Listings from "@/Components/Listings/Listings";
import "./Search.scss";

const Search = () => {

    return (
        <div className="searchPage">
            <div className="mainPage">
                <Header />
                <SearchNavigation />
                <Listings />
            </div>
            <RightNavigation />
        </div>
    )
}

export default Search;
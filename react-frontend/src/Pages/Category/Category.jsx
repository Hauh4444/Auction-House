import SearchBar from "@//Components/SearchBar/SearchBar";
import LeftNavigation from "@//Components/LeftNavigation/LeftNavigation";
import RightNavigation from "@//Components/RightNavigation/RightNavigation";
import "./Category.scss";

const Search = () => {

    return (
        <div className="categoryPage">
            <div style={{height: "100%", display: "flex", flexDirection: "row"}}>
                <LeftNavigation />
                <div style={{flexBasis: "70%"}}>
                    <SearchBar />
                    <div className="mainPage">

                    </div>
                </div>
                <RightNavigation />
            </div>
        </div>
    )
}

export default Search;
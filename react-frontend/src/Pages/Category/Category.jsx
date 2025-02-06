import Header from "@/Components/Header/Header";
import SearchNavigation from "@/Components/SearchNavigation/SearchNavigation.jsx";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import "./Category.scss";

const Category = () => {

    return (
        <div className="categoryPage">
            <div className="mainPage">
                <Header />
                <SearchNavigation />
            </div>
            <RightNavigation />
        </div>
    )
}

export default Category;
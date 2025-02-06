import Header from "@/Components/Header/Header";
import CategoryNavigation from "@/Components/CategoryNavigation/CategoryNavigation";
import RightNavigation from "@/Components/RightNavigation/RightNavigation";
import "./Category.scss";

const Category = () => {

    return (
        <div className="categoryPage">
            <div className="mainPage">
                <Header />
                <CategoryNavigation />
            </div>
            <RightNavigation />
        </div>
    )
}

export default Category;
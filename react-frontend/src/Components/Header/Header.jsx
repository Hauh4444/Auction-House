import { Link } from 'react-router-dom';
import SearchBar from '../SearchBar/SearchBar';
import Navigation from '../Navigation/Navigation';
import Button from '@mui/material/Button'
import './Header.scss';

const Header = () => {
    return (
        <div className="header">
            <Link to="/" className="logo">
                Home
            </Link>
            <SearchBar />
            <Button className="headerBtn">Sign In</Button>
            <Navigation />
        </div>
    )
};

export default Header;
// External Libraries
import PropTypes from "prop-types";
// Stylesheets
import "./Specifics.scss";

const Specifics = ({listing}) => {

    return (
        <div className="specifics">
            {listing.item_specifics && (
                JSON.parse(listing.item_specifics) instanceof Object ? (
                    !Array.isArray(JSON.parse(listing.item_specifics)) ? (
                        <table>
                            <caption>Item Specifics</caption>
                            <tbody>
                            {Object.keys(JSON.parse(listing.item_specifics)).map((key, index) =>
                                <tr key={index}>
                                    <th>{key}</th>
                                    <td>{JSON.parse(listing.item_specifics)[key]}</td>
                                </tr>
                            )}
                            </tbody>
                        </table>
                    ) : (
                        <ul>
                            {Object.keys(JSON.parse(listing.item_specifics)).map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    )
                ) : (
                    <p>{listing.item_specifics}</p>
                )
            )}
        </div>
    )
}

Specifics.propTypes = {
    listing: PropTypes.shape({
        item_specifics: PropTypes.string,
    }),
};

export default Specifics;
// External Libraries
import PropTypes from "prop-types";

// Stylesheets
import "./Specifics.scss";

/**
 * Specifics component displays detailed item-specific information for a given listing.
 *
 * Features:
 * - Parses and displays item specifics from a JSON string.
 * - If item specifics contain key-value pairs, they are displayed in a table format.
 * - If item specifics are an array, they are displayed as a list.
 * - If item specifics are a plain string, they are shown as a paragraph.
 *
 * @param {Object} props - Component props.
 * @param {Object} props.listing - The listing object containing item specifics.
 * @param {string} props.listing.item_specifics - A JSON-encoded string of item specifics.
 *
 * @returns {JSX.Element} A section displaying the item's specific details.
 */
const Specifics = ({ listing }) => {
    return (
        <div className="specifics">
            {listing.item_specifics && (
                // Check if item_specifics is a parsed object
                JSON.parse(listing.item_specifics) instanceof Object ? (
                    // If it's not an array, display as a table of key-value pairs
                    !Array.isArray(JSON.parse(listing.item_specifics)) ? (
                        <table>
                            <caption>Item Specifics</caption>
                            <tbody>
                            {Object.keys(JSON.parse(listing.item_specifics)).map((key, index) => (
                                <tr key={index}>
                                    <th>{key}</th>
                                    <td>{JSON.parse(listing.item_specifics)[key]}</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    ) : (
                        // If it's an array, display each item as a list
                        <ul>
                            {Object.keys(JSON.parse(listing.item_specifics)).map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    )
                ) : (
                    // If it's a plain string, display it as a paragraph
                    <p>{listing.item_specifics}</p>
                )
            )}
        </div>
    );
};

// Define the expected shape of the listing prop
Specifics.propTypes = {
    listing: PropTypes.shape({
        item_specifics: PropTypes.string,
    }),
};

export default Specifics;

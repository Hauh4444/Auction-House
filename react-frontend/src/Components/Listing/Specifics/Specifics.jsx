// External Libraries
import PropTypes from "prop-types";

// Stylesheets
import "./Specifics.scss";

/**
 * Specifics component displays detailed item-specific information for a given listing.
 *
 * @param {Object} props - Component props.
 * @param {Object} props.listing - The listing object containing item specifics.
 * @param {string} props.listing.item_specifics - A JSON-encoded string of item specifics.
 *
 * @returns {JSX.Element} A section displaying the item"s specific details.
 */
const Specifics = ({ listing }) => {
    let itemSpecifics = null;

    // Try to parse item_specifics safely, if it"s a JSON string
    try {
        itemSpecifics = JSON.parse(listing.item_specifics);
    } catch (e) {
        // If it fails, keep itemSpecifics as the original string
        itemSpecifics = listing.item_specifics;
    }

    return (
        <div className="specifics">
            {itemSpecifics && (
                // Check if item_specifics is an object (or array)
                typeof itemSpecifics === "object" ? (
                    // If it"s an array, display as a list
                    Array.isArray(itemSpecifics) ? (
                        <ul>
                            {itemSpecifics.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    ) : (
                        // If it"s an object, display as a table of key-value pairs
                        <table>
                            <caption>Item Specifics</caption>
                            <tbody>
                            {Object.keys(itemSpecifics).map((key, index) => (
                                <tr key={index}>
                                    <th>{key}</th>
                                    <td>{itemSpecifics[key]}</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    )
                ) : (
                    // If it"s a plain string, display it as a paragraph
                    <p>{itemSpecifics}</p>
                )
            )}
        </div>
    );
};

Specifics.propTypes = {
    listing: PropTypes.shape({
        item_specifics: PropTypes.string,
    }),
};

export default Specifics;

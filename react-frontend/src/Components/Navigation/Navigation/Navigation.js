/**
 * toggleNav Function
 *
 * This function manages the selected state of navigation buttons by
 * removing the "selected" class from all buttons and adding it to the
 * button that triggered the event. This provides visual feedback to
 * the user, indicating which navigation option is currently active.
 *
 * Features:
 * - Resets the selected state of all navigation buttons.
 * - Highlights the button that was clicked, improving user experience.
 *
 * @param {Event} e - The event object representing the click event,
 *                    which contains information about the clicked element.
 */
function toggleNav(e) {
    // Remove "selected" class from all buttons
    document.querySelectorAll(".navBtn").forEach(element => {
        element.classList.remove("selected");
    });

    // Add "selected" class to the clicked button
    e.target.classList.add("selected");
}

export default toggleNav;


function toggleNav(e) {
    document.querySelectorAll(".navBtn").forEach(element => {
        element.classList.remove("selected")
    });
    e.target.classList.add("selected");
}

export default toggleNav;
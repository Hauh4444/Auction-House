import { describe, test, expect, beforeEach } from "vitest";
import toggleNav from "./Navigation";

// Set up a mock DOM environment for testing
document.body.innerHTML = `
  <button class="navBtn" id="btn1">Button 1</button>
  <button class="navBtn" id="btn2">Button 2</button>
  <button class="navBtn" id="btn3">Button 3</button>
`;

describe("toggleNav function", () => {
    let buttons;

    beforeEach(() => {
        // Reset button states before each test
        buttons = document.querySelectorAll(".navBtn");
        buttons.forEach(btn => btn.classList.remove("selected"));
    });

    test("should add 'selected' class to the clicked button", () => {
        const event = { target: buttons[1] };
        toggleNav(event);

        expect(buttons[1].classList.contains("selected")).toBe(true);
    });

    test("should remove 'selected' class from all other buttons", () => {
        buttons[0].classList.add("selected"); // Initially selected button
        const event = { target: buttons[2] };
        toggleNav(event);

        expect(buttons[0].classList.contains("selected")).toBe(false);
        expect(buttons[2].classList.contains("selected")).toBe(true);
    });
});

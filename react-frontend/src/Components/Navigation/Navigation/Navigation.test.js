// Testing Libraries
import { describe, expect, beforeEach, test } from "vitest";
import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import toggleNav from "./Navigation";

// Set up a mock DOM environment for testing
document.body.innerHTML = `
  <button class="navBtn" id="btn1" data-testid="navBtn">Button 1</button>
  <button class="navBtn" id="btn2" data-testid="navBtn">Button 2</button>
  <button class="navBtn" id="btn3" data-testid="navBtn">Button 3</button>
`;

describe("toggleNav function", () => {
    let buttons;

    beforeEach(() => {
        // Reset button states before each test
        buttons = screen.queryAllByTestId("navBtn");
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

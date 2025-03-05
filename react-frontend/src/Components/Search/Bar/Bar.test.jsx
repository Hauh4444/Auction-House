// External Libraries
import { MemoryRouter } from "react-router-dom";

// Testing Libraries
import { vi, describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom"

// Internal Modules
import Bar from "./Bar";

// Mock useNavigate before the tests
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async (importOriginal) => {
    const actual = await importOriginal();
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

describe("Bar Component", () => {
    beforeEach(() => {
        mockNavigate.mockClear();
    });

    it("renders search bar input and button", () => {
        render(
            <MemoryRouter>
                <Bar />
            </MemoryRouter>
        );
        // Check if the input and button are rendered
        expect(screen.queryByPlaceholderText("Search")).toBeInTheDocument();
        expect(screen.queryByRole("button")).toBeInTheDocument();
    });

    it("navigates to the home page when search input is empty", () => {
        render(
            <MemoryRouter>
                <Bar />
            </MemoryRouter>
        );

        // Set the input value to be empty (already default state)
        fireEvent.click(screen.queryByRole("button")); // Trigger the search button click

        // Expect navigate to have been called with the home page params
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/",
            search: "nav=view-all", // Default view on home page
        });
    });

    it("navigates to the search results page with the query when search input is not empty", () => {
        render(
            <MemoryRouter>
                <Bar />
            </MemoryRouter>
        );

        // Set the query to a non-empty value
        fireEvent.change(screen.queryByPlaceholderText("Search"), {
            target: { value: "category" },
        });

        fireEvent.click(screen.queryByRole("button")); // Trigger the search button click

        // Expect navigate to have been called with the search page params
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "query=category&start=0&range=10&nav=best-results",
        });
    });

    it("navigates to the search results page when Enter key is pressed", () => {
        render(
            <MemoryRouter>
                <Bar />
            </MemoryRouter>
        );

        // Set the query to a non-empty value
        fireEvent.change(screen.queryByPlaceholderText("Search"), {
            target: { value: "category" },
        });

        // Trigger the Enter keydown event
        fireEvent.keyDown(screen.queryByPlaceholderText("Search"), {
            key: "Enter",
        });

        // Expect navigate to have been called with the correct search page params, including the "?"
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "query=category&start=0&range=10&nav=best-results", // Ensure the "?" is included here
        });
    });
});

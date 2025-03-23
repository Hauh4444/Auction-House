// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import { beforeEach, vi, describe, it, expect } from "vitest";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import Header from "./Header";

// Mocking axios to return mock data for categories
vi.mock("axios");

// Mock useNavigate before the tests
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async (importOriginal) => {
    const actual = await importOriginal();
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

describe("Header Component", () => {
    // Mock categories response
    const mockCategories = {
        data: {
            categories: [
                { category_id: 1, name: "Category 1", image_encoded: "" },
                { category_id: 2, name: "Category 2", image_encoded: "" },
            ]
        }
    };

    // Before each test, mock the axios request
    beforeEach(() => {
        axios.get = vi.fn().mockResolvedValue(mockCategories);
    });

    it("renders the header component correctly", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <Header />
                </MemoryRouter>
            );
        })

        // Check if the navigation buttons are rendered
        expect(screen.queryByText("Home")).toBeInTheDocument();
        expect(screen.queryByText("Shop All")).toBeInTheDocument();
        expect(screen.queryByText("About")).toBeInTheDocument();
        expect(screen.queryByText("Contact")).toBeInTheDocument();
        expect(screen.queryByPlaceholderText("Search")).toBeInTheDocument();
        expect(screen.queryByTestId("searchBtn")).toBeInTheDocument();
    });

    it("renders the 'Categories' button when not on the homepage", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/some-page"]}>
                    <Header/>
                </MemoryRouter>
            );
        })

        // Ensure the Categories button is rendered when not on the homepage
        expect(screen.queryByText("Categories")).toBeInTheDocument();
    });

    it("does not render the 'Categories' button on the homepage", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/"]}>
                    <Header/>
                </MemoryRouter>
            );
        })

        // Ensure the Categories button is not rendered when on the homepage
        expect(screen.queryByText("Categories")).not.toBeInTheDocument();
    });

    it("toggles categories popup when Categories button is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/some-page"]}>
                    <Header/>
                </MemoryRouter>
            );
        })

        const categoriesButton = screen.queryByText("Categories");

        // After clicking the Categories button, the popup should appear
        fireEvent.click(categoriesButton);

        // Wait for the state update (waiting for categories to be fetched)
        await waitFor(() => {
            const categoryNav = screen.getByTestId("categoryNav");
            expect(categoryNav).toHaveStyle("maxHeight: 100%");
        });

        // Toggle the popup again
        fireEvent.click(categoriesButton);

        // After the second click, the popup should have maxHeight: 0
        await waitFor(() => {
            const categoryNav = screen.getByTestId("categoryNav");
            expect(categoryNav).toHaveStyle("maxHeight: 0");
        });
    });

    it("navigates to the home page when search input is empty", () => {
        render(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );

        // Set the input value to be empty (already default state)
        fireEvent.click(screen.queryByTestId("searchBtn")); // Trigger the search button click

        // Expect navigate to have been called with the home page params
        expect(mockNavigate).toHaveBeenCalledWith("/");
    });

    it("navigates to the search results page with the query when search input is not empty", () => {
        render(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );

        // Set the query to a non-empty value
        fireEvent.change(screen.queryByPlaceholderText("Search"), {
            target: { value: "category" },
        });

        fireEvent.click(screen.queryByTestId("searchBtn")); // Trigger the search button click

        // Expect navigate to have been called with the search page params
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "query=category&start=0&range=10&nav=best-results",
        });
    });

    it("navigates to the search results page when Enter key is pressed", () => {
        render(
            <MemoryRouter>
                <Header />
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

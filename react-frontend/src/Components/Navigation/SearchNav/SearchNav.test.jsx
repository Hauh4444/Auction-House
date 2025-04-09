// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import { vi, describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import SearchNav from "./SearchNav";

// Mock axios request
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

describe("SearchNav Component", () => {
    // Before each test, mock the axios request
    beforeEach(() => {
        axios.get = vi.fn().mockResolvedValue({
            data: {
                categories: []
            }
        });
    });

    it("renders the navigation buttons correctly", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        // Check if the navigation buttons are rendered
        expect(screen.queryByText("Best Results")).toBeInTheDocument();
        expect(screen.queryByText("Best Sellers")).toBeInTheDocument();
        expect(screen.queryByText("New")).toBeInTheDocument();
        expect(screen.queryByText("View All")).toBeInTheDocument();
        expect(screen.queryByText("Filters")).toBeInTheDocument();
    });

    it("highlights the correct button based on query parameters", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={ ["/search?nav=best-sellers"] }>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        // Check if the "Best Sellers" button is highlighted by default (based on the query parameter nav)
        const bestSellersBtn = screen.queryByTestId("bestSellersBtn");
        expect(bestSellersBtn).toHaveClass("selected");
    });

    it("navigates to the best results navigation and updates the URL query parameters when best results is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        // Simulate clicking the "Best Results" button
        fireEvent.click(screen.queryByTestId("bestResultsBtn"));

        // Ensure navigate was called with the correct query parameters
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "start=0&range=10&nav=best-results",
        });
    });

    it("navigates to the best sellers navigation and updates the URL query parameters when best sellers is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        // Simulate clicking the "Best Sellers" button
        fireEvent.click(screen.queryByTestId("bestSellersBtn"));

        // Ensure navigate was called with the correct query parameters
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "start=0&range=10&nav=best-sellers",
        });
    });

    it("navigates to the new navigation and updates the URL query parameters when new is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        // Simulate clicking the "New" button
        fireEvent.click(screen.queryByTestId("newBtn"));

        // Ensure navigate was called with the correct query parameters
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "start=0&range=10&nav=new",
        });
    });

    it("navigates to the view all navigation and updates the URL query parameters when view all is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        // Simulate clicking the "View All" button
        fireEvent.click(screen.queryByTestId("viewAllBtn"));

        // Ensure navigate was called with the correct query parameters
        expect(mockNavigate).toHaveBeenCalledWith({
            pathname: "/search",
            search: "page=1&start=0&range=10&nav=view-all",
        });
    });

    it("toggles the filter popup visibility when the Filters button is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <SearchNav/>
                </MemoryRouter>
            );
        })

        const filtersBtn = screen.queryByTestId("filtersBtn");
        // After clicking the Categories button, the popup should appear
        fireEvent.click(filtersBtn);

        // Wait for the state update (waiting for categories to be fetched)
        await waitFor(() => {
            const categoryNav = screen.queryByTestId("filtersPopup");
            expect(categoryNav).toHaveStyle("maxHeight: 100%");
        });

        // Toggle the popup again
        fireEvent.click(filtersBtn);

        // After the second click, the popup should have maxHeight: 0
        await waitFor(() => {
            const categoryNav = screen.queryByTestId("filtersPopup");
            expect(categoryNav).toHaveStyle("maxHeight: 0");
        });
    });
});

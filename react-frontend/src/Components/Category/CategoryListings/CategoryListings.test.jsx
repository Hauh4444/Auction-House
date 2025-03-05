// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import { beforeEach, vi, describe, it, expect } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import CategoryListings from "./CategoryListings";

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

describe("CategoryListings component", () => {
    // Mock Listings for different pages
    const mockListings = {
        data: {
            listings: [
                {
                    listing_id: 1,
                    title_short: "Product 1",
                    buy_now_price: 29.99,
                    image_encoded: "fake_image_data",
                    average_review: 4.5,
                    total_reviews: 12,
                },
                {
                    listing_id: 2,
                    title_short: "Product 2",
                    buy_now_price: 19.99,
                    image_encoded: "fake_image_data_2",
                    average_review: 3.0,
                    total_reviews: 5,
                },
            ],
        }
    };

    // Before each test, mock the axios request
    beforeEach(() => {
        axios.get = vi.fn(() => {
            return Promise.resolve(mockListings); // Page 1
        });
    });

    it("should render the listings correctly", async () => {
        // Test for Page 1
        render(
            <MemoryRouter initialEntries={["/category?category_id=1&page=1"]}>
                <CategoryListings />
            </MemoryRouter>
        );

        // Wait for the listings to load
        await waitFor(() => screen.queryByText("Product 1"));

        // Check that the first product is displayed correctly
        expect(screen.queryByText("Product 1")).toBeInTheDocument();
        expect(screen.queryByText("$29.99")).toBeInTheDocument();

        // Check that the second product is displayed correctly
        expect(screen.queryByText("Product 2")).toBeInTheDocument();
        expect(screen.queryByText("$19.99")).toBeInTheDocument();
    });

    it("should navigate to listing details page when a product is clicked", async () => {
        render(
            <MemoryRouter initialEntries={["/category?category_id=1"]}>
                <CategoryListings />
            </MemoryRouter>
        );

        // Wait for listings to load
        await waitFor(() => screen.queryByText("Product 1"));

        // Click on the first product
        fireEvent.click(screen.queryByText("Product 1"));

        // Check that we navigate to the listing details page
        expect(mockNavigate).toHaveBeenCalledWith("/listing?key=1");
    });

    it("should display the correct number of stars and reviews", async () => {
        render(
            <MemoryRouter initialEntries={["/category?category_id=1"]}>
                <CategoryListings />
            </MemoryRouter>
        );

        // Wait for the listings to load
        await waitFor(() => screen.queryByText("Product 1"));

        const filledStars = screen.queryAllByTestId("filledStar");

        expect(filledStars.length).toBe(7);

        const halfStars = screen.queryAllByTestId("halfStar");
        expect(halfStars.length).toBe(1);

        // Check if total reviews are displayed correctly
        expect(screen.queryByText("12")).toBeInTheDocument();
    });
});

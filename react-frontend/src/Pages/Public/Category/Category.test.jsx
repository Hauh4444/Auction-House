// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import { beforeEach, vi, describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";

// Interal Modules
import Category from "./Category";

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

describe("Category component", () => {
    const mockCategories = {
        data: {
            categories: [
                { category_id: 1, name: "Electronics", image_encoded: "fake_image_data" }
            ],
        },
    };

    const mockCategory = {
        data: {
            category: {
                name: "Electronics",
                description: "Latest gadgets and devices.",
                image_encoded: "fake_image_data",
            }
        }
    }

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
    }

    // Before each test, mock the axios request
    beforeEach(() => {
        axios.get = vi.fn((url) => {
            if (url === `${import.meta.env.BACKEND_URL}/categories/1/`) {
                return Promise.resolve(mockCategory);
            }
            else if (url === `${import.meta.env.BACKEND_URL}/categories/`) {
                return Promise.resolve(mockCategories);
            }
            else if (url === `${import.meta.env.BACKEND_URL}/listings/`) {
                return Promise.resolve(mockListings);
            }
        });
    });

    it("renders category data correctly", async () => {
        render(
            <MemoryRouter initialEntries={["/category?category_id=1&page=1"]}>
                <Category />
            </MemoryRouter>
        );

        await waitFor(() => screen.queryByText("Electronics"));

        expect(screen.queryByTestId("categoryName").innerHTML).toBe("Electronics");
        expect(screen.queryByTestId("categoryDescription").innerHTML).toBe("Latest gadgets and devices.");
        expect(screen.queryByTestId("categoryImage").src).toBe("data:image/jpg;base64,fake_image_data");
    });
});

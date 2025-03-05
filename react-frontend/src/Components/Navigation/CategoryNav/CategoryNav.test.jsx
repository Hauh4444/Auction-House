// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import { beforeEach, vi, describe, it, expect } from "vitest";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import CategoryNav from "./CategoryNav";

// Mock axios
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

describe("CategoryNav Component", () => {
    const mockCategories = {
        data: {
            categories: [
                { category_id: 1, name: "Category 1", image_encoded: "mockBase64ImageData" },
                { category_id: 2, name: "Category 2", image_encoded: null },
            ],
        },
    };

    beforeEach(() => {
        axios.get = vi.fn().mockResolvedValue(mockCategories);
        mockNavigate.mockClear();
    });

    it("fetches and displays categories", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/some-page"]}>
                    <CategoryNav />
                </MemoryRouter>
            );
        });

        await waitFor(() => {
            expect(screen.queryByText("Category 1")).toBeInTheDocument();
            expect(screen.queryByText("Category 2")).toBeInTheDocument();
        });
    });

    it("navigates to the correct category when a category button is clicked", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/some-page"]}>
                    <CategoryNav />
                </MemoryRouter>
            );
        });

        const categoryButton = await screen.findByText("Category 1");
        fireEvent.click(categoryButton);

        expect(mockNavigate).toHaveBeenCalledWith("/category?category_id=1&page=1");
    });

    it("renders category list and not category navigation on the homepage", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/"]}>
                    <CategoryNav />
                </MemoryRouter>
            );
        });

        const categoryContainer = screen.queryByTestId("categoryNav");
        expect(categoryContainer).not.toBeInTheDocument();

        const categoryList = screen.queryByTestId("categoryList");
        expect(categoryList).toBeInTheDocument();
    });

    it("renders category navigation and not category list on non-homepage", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/some-page"]}>
                    <CategoryNav />
                </MemoryRouter>
            );
        });

        const categoryContainer = screen.queryByTestId("categoryNav");
        expect(categoryContainer).toBeInTheDocument();

        const categoryList = screen.queryByTestId("categoryList");
        expect(categoryList).not.toBeInTheDocument();
    });

    it("renders category image when image_encoded exists", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/"]}>
                    <CategoryNav />
                </MemoryRouter>
            );
        });

        const image = screen.queryByAltText("Category 1");
        expect(image).toBeInTheDocument();
        expect(image).toHaveAttribute("src", expect.stringContaining("data:image/jpg;base64,mockBase64ImageData"));
    });

    it("shows fallback text when image_encoded is null", async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={["/"]}>
                    <CategoryNav />
                </MemoryRouter>
            );
        });

        expect(screen.queryByText("No image available")).toBeInTheDocument();
    });
});

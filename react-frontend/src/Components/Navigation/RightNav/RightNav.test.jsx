// External Libraries
import { MemoryRouter } from "react-router-dom";

// Testing Libraries
import { vi, describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import RightNav from "./RightNav";

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

describe("RightNav Component", () => {
    it("renders correctly", () => {
        render(
            <MemoryRouter>
                <RightNav />
            </MemoryRouter>
        );

        // Check if the button elements are rendered
        expect(screen.queryByTestId("menuBtn")).toBeInTheDocument();
        expect(screen.queryByTestId("accountBtn")).toBeInTheDocument();
        expect(screen.queryByTestId("flagBtn")).toBeInTheDocument();
        expect(screen.queryByTestId("cartBtn")).toBeInTheDocument();
        expect(screen.queryByTestId("friendBtn")).toBeInTheDocument();
        expect(screen.queryByTestId("truckBtn")).toBeInTheDocument();
    });

    it("navigates to the account page when account button is clicked", () => {
        render(
            <MemoryRouter>
                <RightNav />
            </MemoryRouter>
        );

        // Simulate a click on the account button
        fireEvent.click(screen.queryByTestId("accountBtn"));

        // Ensure navigate was called with the correct URL
        expect(mockNavigate).toHaveBeenCalledWith("/user/account");
    });
});

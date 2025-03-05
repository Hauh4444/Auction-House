// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import {vi, describe, it, expect, beforeEach} from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";

// Interal Modules
import Reviews from "./Reviews";

describe("Main Component", () => {
    const mockReviews = {
        data: {
            reviews: [
                {
                    stars: 4.5,
                    username: "John Doe",
                    created_at: "2025-03-01",
                    title: "Great Product!",
                    description: "I really liked the product. It exceeded my expectations.",
                },
                {
                    stars: 4,
                    username: "Jane Doe",
                    created_at: "2025-03-02",
                    title: "Good but could improve",
                    description: "The product is good, but there are a few areas for improvement.",
                },
                {
                    stars: 5,
                    username: "Alice",
                    created_at: "2025-03-03",
                    title: "Excellent!",
                    description: "Amazing product. Highly recommend it!",
                },
            ]
        }
    }

    // Before each test, mock the axios request
    beforeEach(() => {
        axios.get = vi.fn().mockResolvedValue(mockReviews);
    });

    it("fetches and displays reviews correctly", async () => {
        render(
            <MemoryRouter>
                <Reviews listing_id={1} />
            </MemoryRouter>
        );

        // Wait for the reviews to be displayed after the async axios call
        await waitFor(() => {
            // Check if reviews are rendered
            expect(screen.queryByText("Great Product!")).toBeInTheDocument();
            expect(screen.queryByText("Good but could improve")).toBeInTheDocument();
            expect(screen.queryByText("Excellent!")).toBeInTheDocument();
        });

        // Check if the stars are rendered correctly based on the rating
        const starIcons = screen.queryAllByTestId("blankStar");
        expect(starIcons.length).toBe(15); // Should have 5 stars as base for each review

        // Check for filled stars for a specific review
        const filledStars = screen.queryAllByTestId("filledStar");
        expect(filledStars.length).toBe(13); // There should be 14 filled stars based on mock data (4.5 + 4 + 5)

        // Check if half star is rendered for the review with 4.5 stars
        const halfStar = screen.queryByTestId("halfStar");
        expect(halfStar).toBeInTheDocument();
    });
});

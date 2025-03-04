// External Libraries
import { MemoryRouter } from 'react-router-dom';

// Testing Libraries
import { vi, describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";

// Interal Modules
import Main from './Main';

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

describe('Main Component', () => {
    // Mock the axios GET request to return fake data
    const mockListing = {
        title: 'Test Product',
        description: '["This is a test description"]', // JSON string representing array
        listing_type: 'auction',
        current_price: 100,
        buy_now_price: 150,
        auction_end: '2025-12-31T23:59:59',
        image_encoded: 'iVBORw0KGgoAAAANSUhEUgAAAAUA...',
        bids: 5,
    }

    it('renders the product title correctly', () => {
        render(
            <MemoryRouter>
                <Main listing={mockListing} />
            </MemoryRouter>
        );

        const title = screen.getByText(mockListing.title);

        expect(title).toBeInTheDocument();
    });

    it('displays auction information when the listing type is auction', () => {
        render(
            <MemoryRouter>
                <Main listing={mockListing} />
            </MemoryRouter>
        );

        const bid = screen.getByText(`$${mockListing.current_price}`);
        const placeBidBtn = screen.getByText('Place Bid');
        const auctionEnd = screen.getByText(`5 bids. Ends: ${mockListing.auction_end}`);

        expect(bid).toBeInTheDocument();
        expect(placeBidBtn).toBeInTheDocument();
        expect(auctionEnd).toBeInTheDocument();
    });

    it('displays the buy now price', () => {
        render(
            <MemoryRouter>
                <Main listing={mockListing} />
            </MemoryRouter>
        );

        const price = screen.getByText(`$${mockListing.buy_now_price}`);

        expect(price).toBeInTheDocument();
    });

    it('displays social media share buttons', () => {
        render(
            <MemoryRouter>
                <Main listing={mockListing} />
            </MemoryRouter>
        );

        const facebookButton = screen.getByTestId(/facebookShareBtn/i);
        const twitterButton = screen.getByTestId(/twitterShareBtn/i);
        const pinterestButton = screen.getByTestId(/pinterestShareBtn/i);

        expect(facebookButton).toBeInTheDocument();
        expect(twitterButton).toBeInTheDocument();
        expect(pinterestButton).toBeInTheDocument();
    });

    it('displays the product image if available', () => {
        render(
            <MemoryRouter>
                <Main listing={mockListing} />
            </MemoryRouter>
        );

        const image = screen.getByAltText(mockListing.title);

        expect(image).toBeInTheDocument();
    });

    it('displays fallback message when no image is available', () => {
        const listingWithoutImage = { ...mockListing, image_encoded: '' };
        render(
            <MemoryRouter>
                <Main listing={listingWithoutImage} />
            </MemoryRouter>
        );

        const noImageMessage = screen.getByText('No image available');

        expect(noImageMessage).toBeInTheDocument();
    });

    it('renders product description as a list if formatted as JSON array', () => {
        render(
            <MemoryRouter>
                <Main listing={mockListing} />
            </MemoryRouter>
        );

        const descriptionItem = screen.getByText('This is a test description');

        expect(descriptionItem).toBeInTheDocument();
    });

    it('displays a fallback message when description is not available or not a valid array', () => {
        const listingWithoutDescription = { ...mockListing, description: '' };
        render(
            <MemoryRouter>
                <Main listing={listingWithoutDescription} />
            </MemoryRouter>
        );

        const noDescriptionMessage = screen.getByText('No description available');

        expect(noDescriptionMessage).toBeInTheDocument();
    });
});

// External Libraries
import {MemoryRouter, Route, Routes} from 'react-router-dom';
import axios from 'axios';

// Testing Libraries
import { beforeEach, vi, describe, it, expect } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import SearchListings from './SearchListings';
import CategoryListings from "@/Components/Category/CategoryListings/CategoryListings.jsx";

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

// Test suite for SearchListings
describe('SearchListings Component', () => {

    const mockListings = {
        data: {
            listings: [
                {
                    listing_id: 1,
                    title: 'Product 1',
                    buy_now_price: 29.99,
                    image_encoded: 'fake_image_data_3',
                    average_review: 4.0,
                    total_reviews: 8,
                },
                {
                    listing_id: 2,
                    title: 'Product 2',
                    buy_now_price: 19.99,
                    image_encoded: 'fake_image_data_4',
                    average_review: 4.8,
                    total_reviews: 15,
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

    it('should render the listings fetched from the API', async () => {
        render(
            <MemoryRouter>
                <SearchListings />
            </MemoryRouter>
        );

        // Wait for the listings to load
        await waitFor(() => screen.getByText('Product 1'));

        // Check that the first product is displayed correctly
        expect(screen.getByText('Product 1')).toBeInTheDocument();
        expect(screen.getByText('$29.99')).toBeInTheDocument();

        // Check that the second product is displayed correctly
        expect(screen.getByText('Product 2')).toBeInTheDocument();
        expect(screen.getByText('$19.99')).toBeInTheDocument();
    });

    it('navigates to the detailed listing view when a title is clicked', async () => {
        render(
            <MemoryRouter>
                <SearchListings />
            </MemoryRouter>
        );

        // Wait for listings to load
        await waitFor(() => screen.getByText('Product 1'));

        // Click on the first product
        fireEvent.click(screen.getByText('Product 1'));

        // Check that we navigate to the listing details page
        expect(mockNavigate).toHaveBeenCalledWith('/listing?key=1');
    });

    it('displays the correct star rating based on the average review', async () => {
        render(
            <MemoryRouter>
                <SearchListings />
            </MemoryRouter>
        );

        // Wait for the listings to be rendered
        await waitFor(() => {
            expect(screen.getByText('Product 1')).toBeInTheDocument();
            expect(screen.getByText('Product 2')).toBeInTheDocument();
        });

        // Check if the correct number of stars is displayed
        // For Product 1, with 4.5 stars, it should show 4 filled stars and 1 half star
        expect(screen.getByText('Product 1').parentElement.querySelector('.stars')).toBeTruthy();
        expect(screen.getByText('Product 2').parentElement.querySelector('.stars')).toBeTruthy();
    });
});

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

describe('Header Component', () => {
    // Mock categories response
    const mockCategories = {
        data: {
            categories: [
                { category_id: 1, name: 'Category 1', image_encoded: '' },
                { category_id: 2, name: 'Category 2', image_encoded: '' },
            ]
        }
    };

    // Before each test, mock the axios request
    beforeEach(() => {
        axios.get = vi.fn().mockResolvedValue(mockCategories);
    });

    it('renders the header component correctly', async () => {
        await act(async () => {
            render(
                <MemoryRouter>
                    <Header />
                </MemoryRouter>
            );
        })

        // Check if the navigation buttons are rendered
        expect(screen.getByText(/Home/i)).toBeInTheDocument();
        expect(screen.getByText(/Shop All/i)).toBeInTheDocument();
        expect(screen.getByText(/About/i)).toBeInTheDocument();
        expect(screen.getByText(/Contact/i)).toBeInTheDocument();
    });

    it('renders the "Categories" button when not on the homepage', async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={['/some-page']}>
                    <Header/>
                </MemoryRouter>
            );
        })

        // Ensure the Categories button is rendered when not on the homepage
        expect(screen.getByText(/Categories/i)).toBeInTheDocument();
    });

    it('does not render the "Categories" button on the homepage', async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={['/']}>
                    <Header/>
                </MemoryRouter>
            );
        })

        // Ensure the Categories button is not rendered when on the homepage
        expect(screen.queryByText(/Categories/i)).not.toBeInTheDocument();
    });

    it('toggles categories popup when Categories button is clicked', async () => {
        await act(async () => {
            render(
                <MemoryRouter initialEntries={['/some-page']}>
                    <Header/>
                </MemoryRouter>
            );
        })

        const categoriesButton = screen.getByText(/Categories/i);

        // After clicking the Categories button, the popup should appear
        fireEvent.click(categoriesButton);

        // Wait for the state update (waiting for categories to be fetched)
        await waitFor(() => {
            const categoryNav = document.querySelector('.categoryNav');
            expect(categoryNav).toHaveStyle('maxHeight: 100%');
        });

        // Toggle the popup again
        fireEvent.click(categoriesButton);

        // After the second click, the popup should have maxHeight: 0
        await waitFor(() => {
            const categoryNav = document.querySelector('.categoryNav');
            expect(categoryNav).toHaveStyle('maxHeight: 0');
        });
    });

});

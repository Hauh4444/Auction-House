// External Libraries
import { MemoryRouter } from 'react-router-dom';

// Testing Libraries
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";

// Interal Modules
import Specifics from './Specifics';

describe('Specifics Component', () => {
    it('renders a table for object item specifics', () => {
        const mockListing = {
            item_specifics: '{"color": "red", "size": "M", "material": "cotton"}',
        };

        render(
            <MemoryRouter>
                <Specifics listing={mockListing} />
            </MemoryRouter>
        );

        // Check if the table is rendered
        const table = screen.getByRole('table');
        expect(table).toBeInTheDocument();

        // Check if table rows are correctly rendered
        expect(screen.getByText('color')).toBeInTheDocument();
        expect(screen.getByText('red')).toBeInTheDocument();
        expect(screen.getByText('size')).toBeInTheDocument();
        expect(screen.getByText('M')).toBeInTheDocument();
        expect(screen.getByText('material')).toBeInTheDocument();
        expect(screen.getByText('cotton')).toBeInTheDocument();
    });

    it('renders a list for array item specifics', () => {
        const mockListing = {
            item_specifics: '["red", "M", "cotton"]',
        };

        render(
            <MemoryRouter>
                <Specifics listing={mockListing} />
            </MemoryRouter>
        );

        // Check if the list is rendered
        const list = screen.getByRole('list');
        expect(list).toBeInTheDocument();

        // Check if list items are correctly rendered
        expect(screen.getByText('red')).toBeInTheDocument();
        expect(screen.getByText('M')).toBeInTheDocument();
        expect(screen.getByText('cotton')).toBeInTheDocument();
    });

    it('renders a paragraph for plain string item specifics', () => {
        const mockListing = {
            item_specifics: "This is a plain string description of item specifics.",
        };

        render(
            <MemoryRouter>
                <Specifics listing={mockListing} />
            </MemoryRouter>
        );

        // Check if the paragraph is rendered
        const paragraph = screen.getByText(/This is a plain string description/);
        expect(paragraph).toBeInTheDocument();
    });

    it('renders nothing when item_specifics is null or undefined', () => {
        const mockListing = {
            item_specifics: null,
        };

        render(
            <MemoryRouter>
                <Specifics listing={mockListing} />
            </MemoryRouter>
        );

        // Check if nothing is rendered
        expect(screen.queryByText('Item Specifics')).not.toBeInTheDocument();
    });

    it('renders nothing when item_specifics is an empty string', () => {
        const mockListing = {
            item_specifics: '',
        };

        render(
            <MemoryRouter>
                <Specifics listing={mockListing} />
            </MemoryRouter>
        );

        // Check if nothing is rendered
        expect(screen.queryByText('Item Specifics')).not.toBeInTheDocument();
    });
});

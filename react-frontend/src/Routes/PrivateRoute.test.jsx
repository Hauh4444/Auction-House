// External Libraries
import { MemoryRouter, Route, Routes } from "react-router-dom";

// Test Libraries
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import PrivateRoute from "./PrivateRoute";
import { useAuth } from "@/ContextAPI/AuthContext";

// Mock the Auth Context
vi.mock("@/ContextAPI/AuthContext", () => ({
    useAuth: vi.fn(),
}));

describe("PrivateRoute Component", () => {
    it("redirects to /auth-page if user is not authenticated", () => {
        // Mock unauthenticated user
        useAuth.mockReturnValue({ user: null });

        render(
            <MemoryRouter initialEntries={ ["/user/account"] }>
                <Routes>
                    <Route path="/auth-page" element={ <div>Auth Page</div> } />
                    <Route element={ <PrivateRoute /> }>
                        <Route path="/user/account" element={ <div>Account Page</div> } />
                    </Route>
                </Routes>
            </MemoryRouter>
        );

        // Check if the user is redirected
        expect(screen.getByText("Auth Page")).toBeInTheDocument();
    });

    it("renders child routes if user is authenticated", () => {
        // Mock authenticated user
        useAuth.mockReturnValue({ user: { id: 1, name: "John Doe" } });

        render(
            <MemoryRouter initialEntries={ ["/user/account"] }>
                <Routes>
                    <Route path="/auth-page" element={ <div>Auth Page</div> } />
                    <Route element={ <PrivateRoute /> }>
                        <Route path="/user/account" element={ <div>Account Page</div> } />
                    </Route>
                </Routes>
            </MemoryRouter>
        );

        // Ensure the protected content is visible
        expect(screen.getByText("Account Page")).toBeInTheDocument();
    });
});

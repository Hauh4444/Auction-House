// External Libraries
import { MemoryRouter } from "react-router-dom";
import axios from "axios";

// Testing Libraries
import { describe, it, expect, vi, beforeEach } from "vitest";
import { act, render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";

// Internal Modules
import PublicRoutes from "@/Routes/PublicRoutes";
import AuthProvider from "@/ContextAPI/AuthProvider";
import { useAuth } from "@/ContextAPI/AuthContext";

// Mock Axios
vi.mock("axios");

// Mock the Auth Context
vi.mock(import("@/ContextAPI/AuthContext"), async (importOriginal) => {
    const actual = await importOriginal()
    return {
        ...actual,
        useAuth: vi.fn(),
    }
})


// Mock Auth Context
const mockUnauthorized = () => ({
    user: null,
    error: null,
    createAccount: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
});

const mockAuthorized = () => ({
    user: { id: 1, name: "John Doe" },
    error: null,
    createAccount: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
});

const mockStaff = () => ({
    user: { id: 1, name: "John Doe", role: "staff" },
    error: null,
    createAccount: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
});

const mockAdmin = () => ({
    user: { id: 1, name: "John Doe", role: "admin" },
    error: null,
    createAccount: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
});

describe("PublicRoutes Component", () => {
    beforeEach(() => {
        axios.get = vi.fn().mockResolvedValue({ data: { categories: [] } });
    });

    it("renders home page for unauthenticated users", async () => {
        useAuth.mockReturnValue(mockUnauthorized());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("homePage")).toBeInTheDocument();
    });

    it("redirects to auth page if an unauthenticated user tries to access a private route", async () => {
        useAuth.mockReturnValue(mockUnauthorized());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/user/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("authPage")).toBeInTheDocument();
    });

    it("renders user account page if user is authenticated", async () => {
        useAuth.mockReturnValue(mockAuthorized());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/user/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("userAccountPage")).toBeInTheDocument();
    });

    it("redirects to auth page if an unauthenticated user tries to access a staff route", async () => {
        useAuth.mockReturnValue(mockUnauthorized());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/staff/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("authPage")).toBeInTheDocument();
    });

    it("redirects to home page if an authorized user tries to access a staff route without proper privelages", async () => {
        useAuth.mockReturnValue(mockAuthorized());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/staff/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("homePage")).toBeInTheDocument();
    });

    it("renders staff account page if user is authenticated with staff privelages", async () => {
        useAuth.mockReturnValue(mockStaff());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/staff/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("staffAccountPage")).toBeInTheDocument();
    });

    it("redirects to auth page if an unauthenticated user tries to access a admin route", async () => {
        useAuth.mockReturnValue(mockUnauthorized());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/admin/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("authPage")).toBeInTheDocument();
    });

    it("redirects to home page if an authorized user tries ot access an admin route without proper privelages", async () => {
        useAuth.mockReturnValue(mockStaff());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/admin/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("homePage")).toBeInTheDocument();
    });

    it("renders admin account page if user is authenticated with admin privelages", async () => {
        useAuth.mockReturnValue(mockAdmin());

        await act(async () => {
            render(
                <AuthProvider>
                    <MemoryRouter initialEntries={["/admin/account"]}>
                        <PublicRoutes />
                    </MemoryRouter>
                </AuthProvider>
            );
        });

        expect(screen.queryByTestId("adminAccountPage")).toBeInTheDocument();
    });
});

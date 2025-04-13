// External Libraries
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header.jsx";
import RightNav from "@/Components/Navigation/RightNav/RightNav.jsx";

// Stylesheets
import "./SiteSettings.scss";

const defaultSettings = {
    // Store Settings
    site_name: "",
    store_description: "",
    default_currency: "USD",
    default_language: "en",
    timezone: "UTC",
    business_email: "",
    support_email: "",

    // Payment & Pricing
    tax_rate: 0,
    discounts_enabled: true,
    free_shipping_threshold: 0,
    accepted_payment_methods: "Visa, MasterCard, PayPal",
    default_shipping_fee: 0,

    // Maintenance
    maintenance_mode: false,
    maintenance_message: "",
    admin_preview_mode: false,
    allow_new_registrations: true,
    checkout_enabled: true,

    // Inventory & Orders
    low_stock_threshold: 5,
    auto_restock_notifications: true,
    max_order_quantity: 10,

    // Notifications
    order_confirmation_email: true,
    abandoned_cart_email: true,
    newsletter_signup_enabled: true,
    admin_notification_email: "",

    // Security
    require_email_verification: true,
    two_factor_auth: false,
    max_login_attempts: 5,
    password_expiration_days: 365,

    // Localization
    supported_currencies: "USD",
    supported_languages: "en",
    measurement_unit: "kg",
};

const SiteSettings = () => {
    const navigate = useNavigate();

    const [settings, setSettings] = useState(defaultSettings);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get("/api/site-settings").then((res) => {
            setSettings((prev) => ({ ...prev, ...res.data }));
            setLoading(false);
        });
    }, []);

    const handleChange = (e) => {
        const { name, type, checked, value } = e.target;
        setSettings((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : (type === "number" ? parseFloat(value) : value),
        }));
    };

    const handleSubmit = () => {
        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/auth/site-settings/`,
        {
            settings: settings,
        },
        {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
        })
            .then(() => navigate("/admin/account"))
            .catch(err => console.log(err));
    };

    if (loading) return <div className="loading">Loading...</div>;

    const renderInput = (label, name, type = "text") => (
        <div className="form-group">
            <label>{ label }</label>
            {type === "checkbox" ? (
                <input
                    value={ settings[name] }
                    name={ name }
                    type={ type }
                    onChange={ handleChange }
                    checked={ settings[name] }
                />
            ) : (
                <TextField
                    className="textField"
                    value={ type === "number" ? String(settings[name]) : settings[name] }
                    label=""
                    name={ name }
                    type={ type }
                    onChange={ handleChange }
                    variant="outlined"
                    size="small"
                    fullWidth
                />
            )}
        </div>
    );

    return (
        <div className="siteSettingsPage page">
            <div className="mainPage">
                <Header />

                <h1>Site Settings</h1>

                <div className="content">
                    <div className="section">
                        <h2>Store Settings</h2>
                        { renderInput("Site Name", "site_name") }
                        { renderInput("Store Description", "store_description") }
                        { renderInput("Default Currency", "default_currency") }
                        { renderInput("Default Language", "default_language") }
                        { renderInput("Timezone", "timezone") }
                        { renderInput("Business Email", "business_email") }
                        { renderInput("Support Email", "support_email") }
                    </div>

                    <div className="section">
                        <h2>Payment & Pricing</h2>
                        { renderInput("Tax Rate (%)", "tax_rate", "number") }
                        { renderInput("Discounts Enabled", "discounts_enabled", "checkbox") }
                        { renderInput("Free Shipping Threshold", "free_shipping_threshold", "number") }
                        { renderInput("Accepted Payment Methods", "accepted_payment_methods") }
                        { renderInput("Default Shipping Fee", "default_shipping_fee", "number") }
                    </div>

                    <div className="section">
                        <h2>Maintenance & Control</h2>
                        { renderInput("Maintenance Mode", "maintenance_mode", "checkbox") }
                        { renderInput("Maintenance Message", "maintenance_message") }
                        { renderInput("Admin Preview Mode", "admin_preview_mode", "checkbox") }
                        { renderInput("Allow New Registrations", "allow_new_registrations", "checkbox") }
                        { renderInput("Checkout Enabled", "checkout_enabled", "checkbox") }
                    </div>

                    <div className="section">
                        <h2>Inventory & Orders</h2>
                        { renderInput("Low Stock Threshold", "low_stock_threshold", "number") }
                        { renderInput("Auto Restock Notifications", "auto_restock_notifications", "checkbox") }
                        { renderInput("Max Order Quantity", "max_order_quantity", "number") }
                    </div>

                    <div className="section">
                        <h2>Notifications</h2>
                        { renderInput("Order Confirmation Email", "order_confirmation_email", "checkbox") }
                        { renderInput("Abandoned Cart Email", "abandoned_cart_email", "checkbox") }
                        { renderInput("Newsletter Signup Enabled", "newsletter_signup_enabled", "checkbox") }
                        { renderInput("Admin Notification Email", "admin_notification_email") }
                    </div>

                    <div className="section">
                        <h2>Security</h2>
                        { renderInput("Require Email Verification", "require_email_verification", "checkbox") }
                        { renderInput("Two-Factor Auth", "two_factor_auth", "checkbox") }
                        { renderInput("Max Login Attempts", "max_login_attempts", "number") }
                        { renderInput("Password Expiration (Days)", "password_expiration_days", "number") }
                    </div>

                    <div className="section">
                        <h2>Localization</h2>
                        { renderInput("Supported Currencies", "supported_currencies") }
                        { renderInput("Supported Languages", "supported_languages") }
                        { renderInput("Measurement Unit", "measurement_unit") }
                    </div>

                    <div className="section"></div>

                    <div className="endSection">
                        <Button className="saveBtn" onClick={ handleSubmit }>
                            Save Settings
                        </Button>
                    </div>
                </div>
            </div>
            <RightNav />
        </div>
    );
};

export default SiteSettings;

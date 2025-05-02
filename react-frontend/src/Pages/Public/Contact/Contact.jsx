// External Libraries
import { Box, TextField, Button, Paper, Link, List, ListItem, ListItemText } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./Contact.scss";

const Contact = () => {
    return (
        <div className="contactPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <div className="content">
                    <h1>
                        📬 Contact Us
                    </h1>

                    <p>
                        &emsp;&emsp;&emsp;We’d love to hear from you! Whether you have feedback, questions about the platform,
                        or are experiencing issues, feel free to reach out using the form below. Our team is
                        committed to providing a supportive and responsive experience.
                    </p>

                    <p>
                        &emsp;&emsp;&emsp;This platform is actively maintained as part of a Computer Science project, and your input
                        helps us continuously improve. We welcome bug reports, feature suggestions, and all forms
                        of constructive feedback.
                    </p>

                    <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
                        <Box
                            component="form"
                            sx={{ display: "flex", flexDirection: "column", gap: 3 }}
                            noValidate
                            autoComplete="off"
                        >
                            <TextField label="Full Name" name="name" required fullWidth />
                            <TextField label="Email Address" name="email" type="email" required fullWidth />
                            <TextField
                                label="Message"
                                name="message"
                                multiline
                                rows={6}
                                required
                                fullWidth
                            />
                            <Button variant="contained" color="primary" type="submit" size="large">
                                Send Message
                            </Button>
                        </Box>
                    </Paper>

                    <Box sx={{ mt: 6 }}>
                        <h2>
                            📧 Other Ways to Reach Us
                        </h2>
                        <List>
                            <ListItem>
                                <ListItemText
                                    primary="Email"
                                    secondary={
                                        <Link href="mailto:support@gofuckyourself.com">
                                            support@gofuckyourself.com
                                        </Link>
                                    }
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="GitHub"
                                    secondary={
                                        <Link
                                            href="https://github.com/Hauh4444/Auction-House"
                                            target="_blank"
                                            rel="noopener"
                                        >
                                            github.com/Hauh4444/Auction-House
                                        </Link>
                                    }
                                />
                            </ListItem>
                        </List>
                    </Box>
                </div>
            </div>

            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default Contact;

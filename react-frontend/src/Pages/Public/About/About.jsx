// External Libraries
import { Container, Typography, List, ListItem, ListItemText } from "@mui/material";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./About.scss";

const About = () => {
    return (
        <div className="aboutPage page">
            <div className="mainPage">
                {/* Page Header */}
                <Header />

                <div className="content">
                    <h1>
                        About Us
                    </h1>
                    <p>
                        &emsp;&emsp;&emsp;Welcome to our Auction House, a next-generation auction and e-commerce platform built as part of our Computer Science project.
                        This platform merges real-time bidding with traditional e-commerce features, providing a dynamic and secure environment to buy, sell, and bid on unique items.
                    </p>

                    <p>
                        &emsp;&emsp;&emsp;This project integrates complex backend logic, real-time WebSocket communication, secure session management, and modern frontend design.
                        We designed the platform to offer both technical proficiency and a user-centered experience, which is vital for creating real-world applications.
                    </p>

                    <h2>
                        🎯 Our Mission
                    </h2>
                    <p>
                        &emsp;&emsp;&emsp;Our mission is to develop a user-friendly, scalable, and secure platform where individuals can engage in live auctions, manage listings,
                        and make secure transactions. The goal is to make auctions and e-commerce more accessible by removing traditional barriers, making it possible for users
                        to buy, sell, and bid with ease.
                    </p>

                    <p>
                        &emsp;&emsp;&emsp;Through this project, we also aimed to simulate the development cycle of a real-world product, applying software engineering principles
                        and human-computer interaction to create an intuitive user experience.
                    </p>

                    <div className="features-tech-container">
                        <div className="technologies-column">
                            <h2>🛠️ Technologies Used</h2>
                            <List>
                                <ListItem>
                                    <ListItemText
                                        primary="💻 Frontend"
                                        secondary="⚛️ React, 🎨 SCSS, 📦 Material UI"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🔙 Backend"
                                        secondary="🐍 Flask, 🔌 Socket.IO"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🗄️ Database"
                                        secondary="🐬 MySQL"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🔐 Authentication"
                                        secondary="👤 Flask-Login, 🗝️ Flask-Session"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🔗 APIs"
                                        secondary="📊 PostHog, 💳 Stripe, ✉️ MailerSend, 📦 Shippo"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🧰 Other Tools"
                                        secondary="🔄 Axios, 🌐 WebSockets"
                                    />
                                </ListItem>
                            </List>
                        </div>

                        <div className="features-column">
                            <h2>✨ Key Features</h2>
                            <List>
                                <ListItem>
                                    <ListItemText
                                        primary="🕒 Live Auctions"
                                        secondary="Real-time bidding system with automatic updates and countdown timers."
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🛒 E-Commerce Listings"
                                        secondary="Support for both auction-based and fixed-price item sales."
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="🔐 Secure Authentication"
                                        secondary="Session-based login system using Flask-Login and Flask-Session."
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="📦 User Dashboard"
                                        secondary="Access to your bidding history, listed items, and purchase records."
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="📱 Mobile-Friendly UI"
                                        secondary="Fully responsive design for desktops, tablets, and smartphones."
                                    />
                                </ListItem>
                            </List>
                        </div>
                    </div>

                    <h2>
                        👥 Our Team
                    </h2>
                    <p>
                        &emsp;&emsp;&emsp;This project was developed by a team of Computer Science students passionate about web development, user experience, and scalable
                        architecture. Our goal was to simulate a real-world product development cycle—planning, prototyping, deployment, and user feedback.
                    </p>
                    <p>
                        &emsp;&emsp;&emsp;Beyond technical implementation, we prioritized collaboration, version control, and agile workflows, and treated this project as a
                        simulation of a professional software development environment.
                    </p>
                </div>
            </div>

            {/* Right-side Navigation */}
            <RightNav />
        </div>
    );
};

export default About;

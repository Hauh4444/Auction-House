# TODO

## React Frontend
1. Document Components
   1. Header
   2. Listing
   3. Navigation
   4. Search
2. Create Pages
   1. Account Management
   2. User Dashboard
   3. Browse
   4. Review
   5. Product Upload
   6. Seller Profile
3. Implement Functionality
   1. Social Media Sharing
   2. Localization of Currency/Language

## Flask Server
1. Routes
   1. User
   2. User Profile
   3. Reviews
2. Services
   1. User
   2. User Profile
   3. Reviews
3. Data Mappers
   1. User
   2. User Profile
   3. Reviews
4. Entities
   1. User
   2. Staff User
   3. User Profile
   4. Reviews
5. Other
   1. Modularization of Services, Data Mappers, and Entities
   2. Backup/Recovery of Database
   3. Rate Limiting API Requests
   4. Session Based User Authentication

# Dinkleberg's Auction House

## Setup
1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm install` command to install node modules.
3. Run the `npm install react react-router-dom react-icons prop-types vite @mui/material @mui/styled-engine-sc styled-components axios sass` command to install the necessary dependencies.

### Flask Server
1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install flask flask-cors flask-mysql` command to install the necessary dependencies.

## Usage

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm install` command to install node modules.
3. Run the `npm run dev` command to launch the React app.

### Flask Backend
1. In a terminal, change to the `flask-server` directory.
2. If you have Flask installed directly onto your machine:
    1. Run the `flask run --debug` command to run the Flask server.
3. If you have a virtual environment:
    1. Run the `.venv/Scripts/activate` command to activate the virtual environment.
    2. Run the `flask run --debug` command to run the Flask server.

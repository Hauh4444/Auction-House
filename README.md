# Dinkleberg's Auction House

### React Frontend
1. Private Pages
   1. Lists
   2. My Bids
   5. Report
   6. Review
   7. Security
   8. Seller Profile
   9. Live Bid
2. Cart Context
3. Live Bidding Context
4. Localization of Currency/Language
5. Public Pages
   1. Browse
   2. Page Not Found
   3. About
   4. Contact
6. Documentation
7. Testing
   1. Pages
   2. ContextAPI
   3. Routes

### Flask Server
1. Bidding Flow
2. Purchasing Flow
3. Payment Functionality
4. Password Recovery with Email Connection
5. User History
6. Recovery System for Database
7. Verify Authentication for Routes
8. Notifications
9. Documentation
10. Unit Testing
11. Integration Testing

## Setup
1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm install` command to install node modules.
3. Run the `npm install react react-router-dom react-icons react-share prop-types vite @mui/material @mui/styled-engine-sc styled-components axios sass vitest @vitest/coverage-v8 @testing-library/react @testing-library/jest-dom jsdom` command to install the necessary dependencies.

### Flask Server
1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install flask flask-cors flask-login flask-session flask-limiter python-dotenv APScheduler pytest` command to install the necessary dependencies.

## Usage

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm run dev` command to launch the React app.

### React Testing
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm test` command to run tests.

### Flask Backend
1. In a terminal, change to the `flask-server` directory. 
2. Run the `.venv/Scripts/activate` command to activate the virtual environment. 
3. Run the `flask run --debug` command to run the Flask server.

### Flask Testing
1. In a terminal, change to the `flask-server` directory.
2. Run the `pytest tests/ -W ignore::DeprecationWarning` command to run tests.
   1. We are ignoring depreciation warnings since they're for site-packages unrelated to our code.

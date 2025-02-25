# Dinkleberg's Auction House

## Setup
1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm install` command to install node modules.
3. Run the `npm install react react-router-dom react-icons react-share prop-types vite @mui/material @mui/styled-engine-sc styled-components axios sass` command to install the necessary dependencies.

### Flask Server
1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install flask flask-cors flask-mysql flask-login flask-session flask-limiter redis` command to install the necessary dependencies.

## Usage

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm run dev` command to launch the React app.

### Flask Backend
1. In a terminal, change to the `flask-server` directory. 
2. Run the `.venv/Scripts/activate` command to activate the virtual environment. 
3. Run the `flask run --debug` command to run the Flask server.

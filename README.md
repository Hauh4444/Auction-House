# Dinkleberg's Auction House 

## Setup

1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.
2. In a terminal, change to the `react-frontend` directory. 
3. Run the `npm install` command to install node modules. 
4. If you wish to install Flask directly onto your machine:
   1. Run the `pip install Flask` command to install Flask. 
5. If you wish to install Flask using a virtual environment:
   1. In a terminal, change to the `flask-server` directory. 
   2. Run the `python -m venv .venv` command to install a virtual environment. 
   3. Run the `.venv/Scripts/activate` command to activate the virtual environment. 
   4. Run the `pip install Flask` command to install Flask into the virtual environment.

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
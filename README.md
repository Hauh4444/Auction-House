# Auction House

## TODO

### React Frontend

- Documentation
- Analytics & Reports
- Order & Delivery API
- Live Auction UI
- Manage Listings
- Implement Feedback UI
- Friend UI

### Flask Server

- Code Review
    - Routes
        - Write & Log Checks for if Data Contains all Necessary Values
    - Data Mappers
        - SQL Statement Consistency
        - SQL Injection Vulnerabilities
    - Entities
        - Setters & Getters
        - Value & Type Checks for Setters
    - Documentation
- Fix Tests
- Analytics & Reports
- Order & Delivery API
- Text Notifications

## Setup

### React Frontend

1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.
2. In a terminal, change to the `react-frontend` directory.
3. Run the `npm install` command to install node modules and required packages within the `package.json` file.

### Flask Server

1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install -r requirements.txt` command to install the necessary dependencies.

### MySQL Database

1. Ensure you have [MySQL Workbench 8.0](https://dev.mysql.com/downloads/installer/) installed on your machine or any other MySQL database management tool.
2. Create a new database.
3. Use the name of this database in the .env file as `DB`.
4. In MySQL Workbench, click on `File` → `Open SQL Script`.
5. Select the required SQL file located in `mysql-database/Data Dumps/`.
6. Press `Ctrl` + `Shift` + `Enter` to run the script and import all tables and data into the database.
7. In MySQL Workbench, click on `Administration` → `Users and Privelages` → `Add Account`.
8. Use the credentials of this account in the .env file as `DB_USER` and `DB_PASSWORD`.

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
3. Run the `python -m app.main` command to run the Flask server.

### Flask Testing

1. In a terminal, change to the `flask-server` directory.
2. Run the `pytest tests/ -W ignore::DeprecationWarning` command to run tests.
    1. We are ignoring depreciation warnings since they're for site-packages unrelated to our code.

### MySQL Database

1. MySQL Workbench will automatically be set to run on startup.
2. You can disable run on startup and manually run using the `net start` command.
3. If you choose any other MySQL database management tool, follow the appropriate guides for usage.

## Other

### MySQL Database

1. There are models for the auctionhouse database located in `mysql-database/Models/` that can be accessed using MySQL Workbench
# Dinkleberg's Auction House

## TODO

1. Messages Page
   1. Need adding friends functionality
      1. Simple add friend button not gonna fuck around with verification
      2. Setup routes and db table
   2. Search friends to create chat
   3. Get chats and chat messages
      1. Backend needs to set viewing_user and other_user via checking session user against user1 and user2 ids
   4. Search chats by username or profile name
2. Support page for users
   1. General support UI
   2. Create support ticket UI
   3. Backend needs to assign support tickets upon creation
   4. Messaging UI for tickets
3. Ticket UI for staff
   1. Messaging UI for tickets
4. User info access UI for staff
   1. UI to access user information
   2. UI to access logs
      1. Backend needs to create logs
   3. Verify backend authentication checks
5. Live auction UI
   1. Page for bidding UI
   2. Proxy bidding
   3. Live updating from the backend
6. View current bids page
7. Email notifications
   1. Notification settings integrated into UI
   2. Email sending on the backend doesn't work right now because fuck you
8. MySQL doesn't have foreign keys setup so do it yourself fucker

## Setup
1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.

### React Frontend
1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm install` command to install node modules and required packages within the `package.json` file.

### Flask Server
1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install -r requirements.txt` command to install the necessary dependencies.

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

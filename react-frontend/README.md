# React Frontend

## Setup

1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.
2. In a terminal, change to the `react-frontend` directory.
3. Run the `npm install` command to install node modules and required packages within the `package.json` file.

## Usage

1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm run dev` command to launch the React app.

## Environment Variables

Create a `.env` file here with the following format:
```dotenv
VITE_FRONTEND_URL=http://localhost:5173 (or whatever frontend url)
VITE_BACKEND_API_URL=http://127.0.0.1:5000/api (or whatever backend api url)
VITE_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
VITE_PUBLIC_POSTHOG_KEY=your_public_posthog_key
VITE_PUBLIC_POSTHOG_HOST=your_public_posthog_host
FAST_REFRESH=false
```

## Testing

1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm test` command to run tests.

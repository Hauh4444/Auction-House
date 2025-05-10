# MySQL Database

## Setup

1. Ensure you have [MySQL Workbench 8.0](https://dev.mysql.com/downloads/installer/) installed on your machine or any other MySQL database management tool.
2. Create a new database.
3. Use the name of this database in the .env file as `DB`.
4. In MySQL Workbench, click on `File` → `Open SQL Script`.
5. Select the required SQL file located in `mysql-database/Data Dumps/`.
6. Press `Ctrl` + `Shift` + `Enter` to run the script and import all tables and data into the database.
7. In MySQL Workbench, click on `Administration` → `Users and Privelages` → `Add Account`.
8. Use the credentials of this account in the .env file as `DB_USER` and `DB_PASSWORD`.

## Usage

1. MySQL Workbench will automatically be set to run on startup.
2. You can disable run on startup and manually run using the `net start MySQL80` command.
3. If you choose any other MySQL database management tool, follow the appropriate guides for usage.

## Other

1. There are models for the auctionhouse database located in `Models/` that can be accessed using MySQL Workbench
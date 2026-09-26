CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    address TEXT NOT NULL.
    email TEXT NOT NULL
);
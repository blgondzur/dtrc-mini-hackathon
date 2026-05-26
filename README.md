# Room Booker

A lightweight, local room booking app that runs entirely on your computer — no cloud, no accounts, no external dependencies. Built with Python's standard library and SQLite.

## Quick Start

```bash
python3 app.py
```

Then open **http://localhost:8765** in your browser.

Your data is stored in `~/.room-booker/bookings.db` and persists between runs.

## Requirements

- Python 3.6+
- A modern web browser
- Internet access (to load the Tailwind CSS stylesheet from CDN on first visit)

## Features

### Role Toggle
A toggle in the top-right corner switches between **Booker** and **Admin** views. No login required.

### Dashboard (both roles)
- Room cards showing name, capacity, location, and amenities
- Live availability summary per room for any selected date
- Booker role shows a **Book This Room** button on each card

### Bookings Tab (both roles)
- All confirmed bookings grouped by date
- Filter between **Upcoming** and **All**
- Hover any row to reveal a **Cancel** button

### Manage Rooms (Admin only)
- Add rooms with name, capacity, location, amenities, and description
- Delete rooms (also removes all associated bookings)

### Booking Modal (Booker)
- Pre-fills the date selected on the dashboard
- Shows existing bookings for the chosen date to help avoid conflicts
- Server-side conflict detection — returns an error if the time slot is already taken
- Remembers your name between sessions

## Project Structure

```
room-booker/
├── app.py        # Python HTTP server + REST API (stdlib only)
├── index.html    # Single-page frontend (vanilla JS + Tailwind CSS)
└── README.md
```

Data is stored separately at `~/.room-booker/bookings.db`.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/rooms` | List all rooms |
| `POST` | `/api/rooms` | Create a room |
| `DELETE` | `/api/rooms/:id` | Delete a room and its bookings |
| `GET` | `/api/bookings` | List confirmed bookings (filterable by `room_id` and `date`) |
| `POST` | `/api/bookings` | Create a booking (checks for conflicts) |
| `PATCH` | `/api/bookings/:id/cancel` | Cancel a booking |

## Tech Stack

- **Backend:** Python 3 standard library (`http.server`, `sqlite3`, `json`)
- **Database:** SQLite via Python's built-in `sqlite3` module
- **Frontend:** Vanilla JavaScript, [Tailwind CSS](https://tailwindcss.com) (loaded from CDN)

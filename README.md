# Room Booker

A lightweight, local room booking app that runs entirely on your computer — no cloud, no accounts, no external dependencies. Built for the WashU DTRC / DI2 summer program with Python's standard library and SQLite.

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

---

### Dashboard (both roles)
- Room cards showing name, capacity, location, and amenities
- **Live status badges** that update automatically every 10 seconds:
  - 🟢 **Free** — no bookings in progress or imminent
  - 🔴 **Occupied** — a booking is currently in progress (shows "Until HH:MM")
  - 🟡 **Coming Up Soon** — a booking starts within the next 30 minutes (shows start time)
- **Live indicator** in the header counts down to the next auto-refresh
- **Date picker** to check availability on any date (live status applies to today only)
- **Time-of-day filter** — set a From/To window to instantly see only rooms free during that slot
- **Book This Room** button on each card (Booker role only)

### Bookings Tab (both roles)
- All confirmed bookings grouped by date
- Filter between **Upcoming** (default) and **All**
- **Cancel** button on every row — room becomes available again immediately

### History Tab (Admin only)
- Full log of every booking ever made, grouped by date (newest first)
- Confirmed bookings shown normally; cancelled bookings shown with strikethrough and a "Cancelled" badge
- Refresh button to pull the latest data

### Manage Rooms Tab (Admin only)
- Add rooms with name, capacity, location, amenities, and optional description
- **Deactivate / Activate** toggle — marks a room inactive without deleting it; inactive rooms are hidden from the dashboard and booking modal
- **Delete** a room (also removes all associated bookings)

### Booking Modal (Booker)
- Opens as a bottom sheet on mobile, centered dialog on desktop
- Pre-fills the date selected on the dashboard
- Shows existing bookings for the chosen date so you can see gaps at a glance
- **Server-side conflict detection** — rejects any booking that overlaps an existing one with a clear inline error message; no silent failures
- Remembers your name between sessions via `localStorage`

---

## Project Structure

```
dtrc-mini-hackathon/
├── app.py        # Python HTTP server + REST API (stdlib only)
├── index.html    # Single-page frontend (vanilla JS + Tailwind CSS)
└── README.md
```

Data is stored separately at `~/.room-booker/bookings.db` (auto-created on first run).

---

## API Reference

| Method | Path | Query params | Description |
|--------|------|-------------|-------------|
| `GET` | `/api/rooms` | `all=1` — include inactive | List rooms (active only by default) |
| `POST` | `/api/rooms` | — | Create a room |
| `PATCH` | `/api/rooms/:id` | — | Toggle `active` status (`{ "active": 0\|1 }`) |
| `DELETE` | `/api/rooms/:id` | — | Delete a room and all its bookings |
| `GET` | `/api/bookings` | `room_id`, `date`, `history=1` | List bookings (`history=1` includes cancelled) |
| `POST` | `/api/bookings` | — | Create a booking (overlap check enforced) |
| `PATCH` | `/api/bookings/:id/cancel` | — | Cancel a booking |

---

## Assignment Checklist

All MUST-HAVE requirements and bonus challenges from the DI2 mini-hackathon prompt are implemented:

| Requirement | Status | Notes |
|---|---|---|
| Add a room (name, floor, capacity) | ✅ | Admin → Manage Rooms |
| Rooms appear in booking view immediately | ✅ | JS state updated without reload |
| Mark rooms inactive | ✅ | Deactivate/Activate toggle; hides from booker view |
| Book a room (date + start/end time) | ✅ | Booking modal on each room card |
| Booking reflects on dashboard immediately | ✅ | Booking pushed to local state on confirm |
| Cancel a booking | ✅ | Cancel button in Bookings tab |
| Live availability dashboard (Free / Occupied / Coming Up Soon) | ✅ | Auto-polls every 10s; live status for today |
| Conflict prevention with clear error | ✅ | SQL overlap check + inline red error message |
| Booking history log [Admin] | ✅ *(bonus)* | History tab with confirmed + cancelled entries |
| Upcoming bookings view [Booker] | ✅ *(bonus)* | Bookings tab defaults to "Upcoming" filter |
| Mobile-friendly layout | ✅ *(bonus)* | Responsive grid, bottom-sheet modal, iOS zoom fix |
| Time-of-day room filtering | ✅ *(bonus)* | From/To filter on dashboard hides occupied rooms |

---

## Tech Stack

- **Backend:** Python 3 standard library (`http.server`, `sqlite3`, `json`)
- **Database:** SQLite via Python's built-in `sqlite3` module
- **Frontend:** Vanilla JavaScript, [Tailwind CSS](https://tailwindcss.com) (loaded from CDN)

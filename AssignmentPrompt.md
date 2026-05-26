DTRC Mini Hackathon Build Something Real, Today
The team who manually figures out which rooms are free is in this room right now. You're not building a demo - you're building a tool your PMs and Tech Leads will actually use this summer.
USER ROLES
PRIZE
Administrator - DI2 staff who manage rooms
• Add rooms: name, floor/location, capacity
• Mark rooms inactive without deleting
& Mini-projector
Booker - PMs & Tech Leads who book
• Book a room for a date & timeslot
• See live availability dashboard
• Cancel their own reservations
No real auth required - a role toggle or separate
Admin vs. Booker view is acceptable.
MUST-HAVE REQUIREMENTS — ship all of these or you don't qualify
• Room management [Admin] - Add a room (name, floor, capacity). Rooms appear in booking view immediately. Admin can mark rooms inactive.
• Room booking [Booker] — Select a room, pick date + start/end time, confirm. Booking reflects on dashboard immediately.
• Cancel a booking [Booker] - Booker can cancel their own reservation. Room becomes available again immediately.
JUDGING CRITERIA
• It works: Core requirements run without crashing during the demo
• Ease of use: A PM can book a room in under 60 seconds without help
• Bonus features: Tiebreaker points for anything beyond the must-haves
• Live availability dashboard [Both] - All active rooms with status: Free, Occupied, or Coming Up Soon (booked within 30 min).
Polling every 10-15s is fine - no
WebSocket needed.
• Conflict prevention [Booker] - Block any booking overlapping an existing reservation.
Show a clear error message — no silent failures.
BONUS CHALLENGES (tiebreakers)
• Booking history log [Admin]
• Upcoming bookings view [Booker]
• Mobile-friendly layout
• Time-of-day room filtering
Pro tip: Use Al tools (Claude, Copilot, Gemini) to scaffold fast — but test everything before the demo. "The Al wrote it" is not an excuse for a crash. Ship simple, ship working.
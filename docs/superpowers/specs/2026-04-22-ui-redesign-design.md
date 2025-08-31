# Trophy Dice Roller — UI Redesign

## Summary

Replace the Vue 3 + Vuetify frontend with a vanilla HTML/CSS/JS app. Drop all framework dependencies. Keep Vite as the bundler and continue serving the build output from FastAPI at `/ui/`.

## Goals

- Minimal dependencies (Vite only)
- Dark, clean aesthetic with gold/amber accents
- Same UX flow: room creation → name input → roll and view results
- Auto-discover roll types from the OpenAPI spec at runtime
- Poll for roll results instead of using Socket.IO

## File Structure

```
ui/
├── index.html
├── style.css
├── src/
│   ├── app.js          # Entry point, orchestrates flow
│   ├── api.js          # OpenAPI discovery + fetch wrapper
│   ├── modals.js       # Room + Name modal logic
│   ├── sidenav.js      # Roll type discovery, roll forms
│   └── rolls.js        # Polling, roll card rendering
├── vite.config.js
└── package.json        # Only dev dependency: vite
```

## UX Flow

1. Page loads at `/ui/` → **Room modal** appears (centered overlay, "Create Room" button)
2. POST `/api/v1/room` → browser navigates to `/ui/:room_uid`
3. **Name modal** appears → user enters display name, stored in JS memory (e.g. a variable or sessionStorage)
4. Main view renders:
   - Trophy RPG logo centered at top
   - Red "Rolls" button fixed top-right
   - Roll results area below the logo
5. Clicking "Rolls" opens a **slide-out side nav** from the right
   - Lists auto-discovered roll types as expandable sections
   - Each section has parameter inputs (number steppers) and a submit button
6. Roll results area polls `GET /api/v1/room/:uid` every 3–5 seconds
   - Renders roll cards with dice images and message HTML
   - New rolls appear at the top

## Visual Design

| Element       | Value                              |
|---------------|------------------------------------|
| Background    | Near-black (`#111`)                |
| Text          | Off-white (`#e0e0e0`)             |
| Accent        | Muted gold/amber (`#c9a84c`)      |
| Action button | Deep red                           |
| Font          | System sans-serif stack            |
| Cards         | Dark (`#1a1a1a`), thin gold border |
| Modals        | Centered, dark semi-transparent backdrop |
| Spacing       | Generous padding throughout        |

## API Integration

### OpenAPI Discovery

- Fetch `/openapi.json` on page load
- Parse paths matching `/api/v*/roll*` patterns
- Extract parameter schemas (names, types, enum values) to dynamically build roll forms
- Each discovered endpoint becomes a section in the side nav

### Roll Submission

- POST to the discovered endpoint with JSON body containing user-provided parameters
- Include display name and room UID in the request

### Sync Polling

- `GET /api/v1/room/:uid` every 3–5 seconds via `setInterval`
- Diff against previously rendered rolls to avoid re-rendering the entire list
- Render dice images from `/dice/` static path and message HTML from the API response

## What Gets Removed

- Vue 3, vue-router, vue-tsc
- Vuetify 3, vite-plugin-vuetify, @mdi/font
- Socket.IO client (socket.io-client)
- swagger-client
- tiny-emitter
- All Vue SFCs (.vue files)
- Server-side Socket.IO handler (trophydice/socketio.py) — confirm with backend whether this can be removed entirely or just left unused

## What Stays

- Vite (as dev dependency and build tool)
- FastAPI static file serving (SinglePageApp at `/ui/`, StaticFiles at `/dice/`)
- All backend API endpoints unchanged
- Trophy RPG logo asset
- Dice image assets in `files/dice/`

## Vite Configuration

- Dev proxy: `/api`, `/openapi.json`, `/dice` → `http://localhost:8000`
- Production base path: `/ui/`
- No framework plugins needed

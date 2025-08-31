# UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Vue 3 + Vuetify frontend with a vanilla HTML/CSS/JS app that has a dark, clean aesthetic with gold accents.

**Architecture:** Single-page vanilla app with a few JS modules. Vite bundles them. FastAPI continues serving the build at `/ui/` with SPA fallback. OpenAPI spec is fetched and parsed with plain `fetch()` to auto-discover roll types.

**Tech Stack:** Vanilla HTML/CSS/JS, Vite 4 (build tool only)

**Worktree:** `/Users/daniel/kiln/worktrees/trophydice-ui-redesign` (branch: `ui-redesign`)

---

### Task 1: Scaffold — package.json and Vite config

**Files:**
- Create: `ui/package.json`
- Create: `ui/vite.config.js`
- Create: `ui/index.html`
- Create: `ui/src/app.js` (empty)
- Create: `ui/src/api.js` (empty)
- Create: `ui/src/modals.js` (empty)
- Create: `ui/src/sidenav.js` (empty)
- Create: `ui/src/rolls.js` (empty)

Replace the existing Vue/Vuetify package.json and vite config with minimal vanilla equivalents. Keep `src/assets/logo.svg` and `public/favicon.ico`.

- [ ] **Step 1: Remove old frontend files, keeping logo and favicon**

```bash
cd /Users/daniel/kiln/worktrees/trophydice-ui-redesign/ui
# Preserve logo and favicon
cp src/assets/logo.svg /tmp/trophy-logo.svg
cp public/favicon.ico /tmp/trophy-favicon.ico

# Remove old source files individually
rm src/main.ts src/App.vue src/swagger.ts src/socket.ts src/eventBus.ts
rm src/plugins/vuetify.js
rm src/components/SideNav.vue src/components/RollType.vue src/components/GenericRoll.vue
rm src/components/RollTable.vue src/components/RollCards.vue src/components/RoomModal.vue
rm src/components/UserModal.vue src/components/NickList.vue src/components/InputNumber.vue
rm src/assets/base.css
rm tsconfig.json tsconfig.vite-config.json env.d.ts .eslintrc.cjs Makefile
rm vite.config.ts package.json package-lock.json
rmdir src/plugins src/components 2>/dev/null || true

# Restore assets
cp /tmp/trophy-logo.svg src/assets/logo.svg
cp /tmp/trophy-favicon.ico public/favicon.ico
```

- [ ] **Step 2: Write new package.json**

```json
{
  "name": "trophydice-ui",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^4.5.0"
  }
}
```

- [ ] **Step 3: Write vite.config.js**

```js
import { defineConfig } from "vite";

export default defineConfig({
  base: process.env.NODE_ENV === "production" ? "/ui/" : "/",
  root: ".",
  build: {
    outDir: "dist",
  },
  server: {
    proxy: {
      "^/(api|openapi.json|dice)": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
```

- [ ] **Step 4: Create index.html**

```html
<\!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Trophy Dice Roller</title>
    <link rel="icon" href="/favicon.ico" />
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body>
    <header>
      <img src="/src/assets/logo.svg" alt="Trophy RPG" class="logo" />
      <button id="rolls-btn" class="btn-rolls">Rolls</button>
    </header>

    <main id="roll-list"></main>

    <div id="sidenav" class="sidenav">
      <div class="sidenav-header">
        <h2>Rolls</h2>
        <button id="sidenav-close" class="sidenav-close">&times;</button>
      </div>
      <div id="sidenav-content"></div>
    </div>
    <div id="sidenav-overlay" class="sidenav-overlay"></div>

    <div id="room-modal" class="modal-overlay">
      <div class="modal">
        <h2>Trophy Dice Roller</h2>
        <p>Create a room to start rolling dice with your group.</p>
        <button id="create-room-btn" class="btn-primary">Create Room</button>
      </div>
    </div>

    <div id="name-modal" class="modal-overlay" style="display:none">
      <div class="modal">
        <h2>What's your name?</h2>
        <input id="name-input" type="text" placeholder="Display name" class="input-field" autocomplete="off" />
        <button id="save-name-btn" class="btn-primary">Save</button>
      </div>
    </div>

    <script type="module" src="/src/app.js"></script>
  </body>
</html>
```

- [ ] **Step 5: Create empty JS module files**

Create these empty files so the project structure is in place:
- `ui/src/app.js`
- `ui/src/api.js`
- `ui/src/modals.js`
- `ui/src/sidenav.js`
- `ui/src/rolls.js`

- [ ] **Step 6: Install and verify Vite starts**

```bash
cd ui && npm install && npx vite --host 0.0.0.0
```

Expected: Vite dev server starts, page loads with the HTML shell (unstyled).

- [ ] **Step 7: Commit**

```bash
git add ui/
git commit -m "scaffold vanilla UI with vite config and HTML shell"
```

---

### Task 2: Style — dark theme with gold accents

**Files:**
- Create: `ui/style.css`

- [ ] **Step 1: Write style.css**

```css
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --bg: #111;
  --bg-card: #1a1a1a;
  --text: #e0e0e0;
  --text-muted: #888;
  --gold: #c9a84c;
  --red: #a33;
  --red-hover: #c44;
  --border: #2a2a2a;
  --overlay: rgba(0, 0, 0, 0.7);
  --radius: 8px;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

html, body {
  height: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* Header */
header {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem 1rem;
  position: relative;
}

.logo {
  display: block;
  width: 100px;
  height: 100px;
}

.btn-rolls {
  position: absolute;
  right: 1rem;
  top: 1.5rem;
  background: var(--red);
  color: #fff;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-rolls:hover {
  background: var(--red-hover);
}

/* Main roll list */
main {
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Roll cards */
.roll-card {
  background: var(--bg-card);
  border: 1px solid var(--gold);
  border-radius: var(--radius);
  padding: 1rem;
}

.roll-card .message {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

.roll-card .message strong {
  color: var(--gold);
}

.roll-card .dice {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.roll-card .dice img {
  height: auto;
  border-radius: 4px;
}

.roll-card .dice img.highest {
  width: 48px;
}

.roll-card .dice img.lower {
  width: 40px;
}

/* Side nav */
.sidenav {
  position: fixed;
  top: 0;
  right: -320px;
  width: 320px;
  height: 100%;
  background: var(--bg-card);
  border-left: 1px solid var(--border);
  z-index: 200;
  transition: right 0.3s ease;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.sidenav.open {
  right: 0;
}

.sidenav-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
}

.sidenav-header h2 {
  color: var(--gold);
  font-size: 1.25rem;
}

.sidenav-close {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.5rem;
  cursor: pointer;
}

.sidenav-overlay {
  position: fixed;
  inset: 0;
  background: var(--overlay);
  z-index: 199;
  display: none;
}

.sidenav-overlay.visible {
  display: block;
}

/* Expansion panels in sidenav */
.roll-section {
  border-bottom: 1px solid var(--border);
}

.roll-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  text-transform: capitalize;
  font-weight: 600;
  color: var(--text);
  transition: color 0.2s;
}

.roll-section-header:hover {
  color: var(--gold);
}

.roll-section-header .chevron {
  transition: transform 0.2s;
  color: var(--text-muted);
}

.roll-section.open .roll-section-header .chevron {
  transform: rotate(180deg);
}

.roll-section-body {
  display: none;
  padding: 0 1.25rem 1rem;
}

.roll-section.open .roll-section-body {
  display: block;
}

/* Form controls */
.param-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.param-row label {
  text-transform: capitalize;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.stepper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stepper button {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stepper button:hover {
  border-color: var(--gold);
}

.stepper .stepper-value {
  width: 2rem;
  text-align: center;
  font-size: 1rem;
  font-weight: 600;
}

.btn-roll {
  width: 100%;
  padding: 0.5rem;
  background: var(--red);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-roll:hover {
  background: var(--red-hover);
}

/* Generic roll color picker */
.color-add-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.color-add-row select {
  flex: 1;
  padding: 0.4rem;
  border-radius: 4px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  font-size: 0.9rem;
}

.color-add-row button {
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  border: 1px solid var(--gold);
  background: transparent;
  color: var(--gold);
  cursor: pointer;
  font-size: 0.9rem;
}

.color-add-row button:hover {
  background: var(--gold);
  color: var(--bg);
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: var(--overlay);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: var(--bg-card);
  border: 1px solid var(--gold);
  border-radius: var(--radius);
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
}

.modal h2 {
  color: var(--gold);
  margin-bottom: 0.75rem;
}

.modal p {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.input-field {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text);
  font-size: 1rem;
  margin-bottom: 1rem;
  outline: none;
}

.input-field:focus {
  border-color: var(--gold);
}

.btn-primary {
  padding: 0.6rem 1.5rem;
  background: var(--red);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: var(--red-hover);
}

/* Responsive */
@media (max-width: 600px) {
  .logo {
    width: 72px;
    height: 72px;
  }

  .roll-card .dice img.highest {
    width: 40px;
  }

  .roll-card .dice img.lower {
    width: 32px;
  }
}
```

- [ ] **Step 2: Verify in browser**

Open the Vite dev server. The HTML shell should render with the dark background, gold-bordered modals, red buttons, and Trophy logo centered.

- [ ] **Step 3: Commit**

```bash
git add ui/style.css
git commit -m "add dark theme with gold accents"
```

---

### Task 3: API module — OpenAPI discovery and fetch wrapper

**Files:**
- Create: `ui/src/api.js`

This module fetches `/openapi.json`, parses it to discover roll endpoints and their parameters, and provides helpers for room creation, roll submission, and roll fetching.

- [ ] **Step 1: Write api.js**

```js
let spec = null;

export async function loadSpec() {
  const resp = await fetch("/openapi.json");
  spec = await resp.json();
  return spec;
}

export function getSpec() {
  return spec;
}

export function discoverRollEndpoints() {
  if (\!spec) throw new Error("Spec not loaded");
  const endpoints = [];

  for (const [path, methods] of Object.entries(spec.paths)) {
    if (\!path.match(/\/api\/v\d+\//)) continue;
    if (path.includes("/room")) continue;

    const method = methods.get ? "GET" : methods.post ? "POST" : null;
    if (\!method) continue;

    const operation = methods.get || methods.post;
    const name = path.split("/").pop();
    const params = [];

    if (method === "GET" && operation.parameters) {
      for (const p of operation.parameters) {
        if (p.in === "query" && p.schema && p.schema.type === "integer") {
          params.push({ name: p.name, required: p.required || false });
        }
      }
    }

    let bodyColors = null;
    if (method === "POST" && operation.requestBody) {
      const content = operation.requestBody.content;
      const jsonSchema =
        content &&
        content["application/json"] &&
        content["application/json"].schema;
      if (jsonSchema && jsonSchema["$ref"]) {
        const refName = jsonSchema["$ref"].split("/").pop();
        const schemaDef =
          spec.components &&
          spec.components.schemas &&
          spec.components.schemas[refName];
        if (schemaDef && schemaDef.properties) {
          bodyColors = Object.keys(schemaDef.properties);
        }
      }
    }

    endpoints.push({
      path,
      method,
      name,
      params,
      bodyColors,
      operationId: operation.operationId,
    });
  }

  return endpoints;
}

export async function createRoom() {
  const resp = await fetch("/api/v1/room", { method: "POST" });
  return resp.json();
}

export async function getRolls(roomUid, seqId) {
  const url = "/api/v1/room/" + roomUid + "?seq_id=" + seqId;
  const resp = await fetch(url);
  return resp.json();
}

export async function submitRoll(endpoint, roomUid, userName, params) {
  const headers = {
    "X-Room": roomUid,
    "X-User-Name": userName,
  };

  if (endpoint.method === "GET") {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value \!== undefined && value \!== 0) query.set(key, String(value));
    }
    const url = endpoint.path + "?" + query.toString();
    const resp = await fetch(url, { headers });
    return resp.json();
  }

  if (endpoint.method === "POST") {
    headers["Content-Type"] = "application/json";
    const resp = await fetch(endpoint.path, {
      method: "POST",
      headers,
      body: JSON.stringify(params),
    });
    return resp.json();
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add ui/src/api.js
git commit -m "add API module with OpenAPI discovery and fetch wrapper"
```

---

### Task 4: Modals — room creation and name input

**Files:**
- Create: `ui/src/modals.js`

- [ ] **Step 1: Write modals.js**

```js
import { createRoom } from "./api.js";

let currentUser = null;

export function getUserName() {
  return currentUser || "Guest";
}

export function getRoomUid() {
  const path = window.location.pathname;
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const remainder = base ? path.replace(base, "") : path;
  const uid = remainder.replace(/^\//, "");
  return uid || null;
}

export function initModals(onReady) {
  const roomModal = document.getElementById("room-modal");
  const nameModal = document.getElementById("name-modal");
  const createBtn = document.getElementById("create-room-btn");
  const saveNameBtn = document.getElementById("save-name-btn");
  const nameInput = document.getElementById("name-input");

  const roomUid = getRoomUid();

  if (roomUid) {
    roomModal.style.display = "none";
    nameModal.style.display = "flex";
  }

  createBtn.addEventListener("click", async () => {
    createBtn.disabled = true;
    createBtn.textContent = "Creating...";
    const room = await createRoom();
    const base = import.meta.env.BASE_URL.replace(/\/$/, "");
    window.location.href = base + "/" + room.uid;
  });

  function saveName() {
    const name = nameInput.value.trim();
    if (\!name) return;
    currentUser = name;
    nameModal.style.display = "none";
    onReady(getRoomUid());
  }

  saveNameBtn.addEventListener("click", saveName);
  nameInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") saveName();
  });
}
```

- [ ] **Step 2: Commit**

```bash
git add ui/src/modals.js
git commit -m "add room creation and name input modals"
```

---

### Task 5: Side nav — roll type discovery and forms

**Files:**
- Create: `ui/src/sidenav.js`

- [ ] **Step 1: Write sidenav.js**

```js
import { discoverRollEndpoints, submitRoll } from "./api.js";
import { getUserName, getRoomUid } from "./modals.js";

let onRollCallback = null;

export function initSideNav(onRoll) {
  onRollCallback = onRoll;

  const sidenav = document.getElementById("sidenav");
  const overlay = document.getElementById("sidenav-overlay");
  const openBtn = document.getElementById("rolls-btn");
  const closeBtn = document.getElementById("sidenav-close");

  function open() {
    sidenav.classList.add("open");
    overlay.classList.add("visible");
  }

  function close() {
    sidenav.classList.remove("open");
    overlay.classList.remove("visible");
  }

  openBtn.addEventListener("click", open);
  closeBtn.addEventListener("click", close);
  overlay.addEventListener("click", close);

  const content = document.getElementById("sidenav-content");
  const endpoints = discoverRollEndpoints();

  for (const ep of endpoints) {
    const section = buildRollSection(ep, close);
    content.appendChild(section);
  }
}

function buildRollSection(endpoint, closeSidenav) {
  const section = document.createElement("div");
  section.className = "roll-section";

  const header = document.createElement("div");
  header.className = "roll-section-header";
  header.innerHTML =
    "<span>" + endpoint.name + '</span><span class="chevron">&#9660;</span>';
  header.addEventListener("click", () => section.classList.toggle("open"));

  const body = document.createElement("div");
  body.className = "roll-section-body";

  const paramValues = {};

  if (endpoint.method === "GET" && endpoint.params.length > 0) {
    for (const p of endpoint.params) {
      paramValues[p.name] = 0;
      body.appendChild(buildStepper(p.name, paramValues));
    }
  }

  if (endpoint.method === "POST" && endpoint.bodyColors) {
    const selectedColors = [];
    const colorRow = document.createElement("div");
    colorRow.className = "color-add-row";

    const select = document.createElement("select");
    function refreshColorOptions() {
      select.innerHTML = "";
      for (const c of endpoint.bodyColors) {
        if (\!selectedColors.includes(c)) {
          const opt = document.createElement("option");
          opt.value = c;
          opt.textContent = c;
          select.appendChild(opt);
        }
      }
    }
    refreshColorOptions();

    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add";
    addBtn.addEventListener("click", () => {
      const color = select.value;
      if (\!color || selectedColors.includes(color)) return;
      selectedColors.push(color);
      paramValues[color] = 1;
      body.insertBefore(buildStepper(color, paramValues), colorRow);
      refreshColorOptions();
    });

    colorRow.appendChild(select);
    colorRow.appendChild(addBtn);
    body.appendChild(colorRow);
  }

  const rollBtn = document.createElement("button");
  rollBtn.className = "btn-roll";
  rollBtn.textContent = "Roll";
  rollBtn.addEventListener("click", async () => {
    const roomUid = getRoomUid();
    if (\!roomUid) return;
    rollBtn.disabled = true;
    rollBtn.textContent = "Rolling...";
    const result = await submitRoll(
      endpoint,
      roomUid,
      getUserName(),
      { ...paramValues }
    );
    if (onRollCallback) onRollCallback(result);
    closeSidenav();
    rollBtn.disabled = false;
    rollBtn.textContent = "Roll";
  });

  body.appendChild(rollBtn);
  section.appendChild(header);
  section.appendChild(body);
  return section;
}

function buildStepper(label, valuesObj) {
  const row = document.createElement("div");
  row.className = "param-row";

  const lbl = document.createElement("label");
  lbl.textContent = label;

  const stepper = document.createElement("div");
  stepper.className = "stepper";

  const minus = document.createElement("button");
  minus.textContent = "\u2212";

  const display = document.createElement("span");
  display.className = "stepper-value";
  display.textContent = String(valuesObj[label] || 0);

  const plus = document.createElement("button");
  plus.textContent = "+";

  minus.addEventListener("click", () => {
    if (valuesObj[label] > 0) {
      valuesObj[label]--;
      display.textContent = String(valuesObj[label]);
    }
  });

  plus.addEventListener("click", () => {
    valuesObj[label]++;
    display.textContent = String(valuesObj[label]);
  });

  stepper.appendChild(minus);
  stepper.appendChild(display);
  stepper.appendChild(plus);
  row.appendChild(lbl);
  row.appendChild(stepper);
  return row;
}
```

- [ ] **Step 2: Commit**

```bash
git add ui/src/sidenav.js
git commit -m "add side nav with dynamic roll type discovery and forms"
```

---

### Task 6: Rolls — polling and card rendering

**Files:**
- Create: `ui/src/rolls.js`

- [ ] **Step 1: Write rolls.js**

```js
import { getRolls } from "./api.js";

let seqId = 0;
let knownUids = new Set();
let pollInterval = null;
let rollList = null;

export function initRolls(roomUid) {
  rollList = document.getElementById("roll-list");
  startPolling(roomUid);
}

function startPolling(roomUid) {
  fetchRolls(roomUid);
  pollInterval = setInterval(() => fetchRolls(roomUid), 4000);
}

async function fetchRolls(roomUid) {
  const data = await getRolls(roomUid, seqId);
  if (data.results && data.results.length > 0) {
    for (const roll of data.results) {
      if (\!knownUids.has(roll.uid)) {
        knownUids.add(roll.uid);
        const card = buildRollCard(roll);
        rollList.prepend(card);
      }
    }
    seqId = data.seq_id;
  }
}

export function addRollImmediately(roll) {
  if (\!rollList) return;
  if (knownUids.has(roll.uid)) return;
  knownUids.add(roll.uid);
  const card = buildRollCard(roll);
  rollList.prepend(card);
}

function buildRollCard(roll) {
  const card = document.createElement("div");
  card.className = "roll-card";

  const msg = document.createElement("div");
  msg.className = "message";
  msg.innerHTML = roll.message;

  const diceRow = document.createElement("div");
  diceRow.className = "dice";

  if (roll.dice) {
    for (const die of roll.dice) {
      const img = document.createElement("img");
      img.src = die.link;
      img.alt = die.dice_type + " " + die.result;
      img.className = die.highest ? "highest" : "lower";
      diceRow.appendChild(img);
    }
  }

  card.appendChild(msg);
  card.appendChild(diceRow);
  return card;
}
```

- [ ] **Step 2: Commit**

```bash
git add ui/src/rolls.js
git commit -m "add roll polling and card rendering"
```

---

### Task 7: App entry point — wire everything together

**Files:**
- Create: `ui/src/app.js`

- [ ] **Step 1: Write app.js**

```js
import { loadSpec } from "./api.js";
import { initModals } from "./modals.js";
import { initSideNav } from "./sidenav.js";
import { initRolls, addRollImmediately } from "./rolls.js";

async function boot() {
  await loadSpec();

  initModals((roomUid) => {
    initSideNav(addRollImmediately);
    initRolls(roomUid);
  });
}

boot();
```

- [ ] **Step 2: Verify the full flow in browser**

Start both the FastAPI backend and the Vite dev server:

```bash
# Terminal 1 (from repo root):
make run

# Terminal 2 (from ui/):
npx vite
```

Test the following:

1. Open the dev URL — Room modal should appear with dark background, gold border
2. Click "Create Room" — should redirect to `/<room-uid>`
3. Name modal appears — enter a name, click Save (or press Enter)
4. Click "Rolls" button (red, top-right) — side nav slides in from right with discovered roll types
5. Expand a roll type, set params with +/- steppers, click Roll — roll card appears in main area
6. Wait 4 seconds — polling picks up the same roll (no duplicate rendered)
7. Open same URL in another tab, enter different name, roll — both tabs see each other's rolls via polling

- [ ] **Step 3: Commit**

```bash
git add ui/src/app.js
git commit -m "wire app entry point connecting all modules"
```

---

### Task 8: Clean up backend — remove Socket.IO

**Files:**
- Delete: `trophydice/socketio.py`
- Modify: `trophydice/app.py` — remove any Socket.IO imports/setup
- Modify: `trophydice/handlers/v1/roll.py` — remove `sm` import and commented-out emit lines
- Modify: `trophydice/handlers/v2/roll.py` — remove `sm` import and commented-out emit lines

- [ ] **Step 1: Delete socketio.py**

```bash
rm trophydice/socketio.py
```

- [ ] **Step 2: Remove Socket.IO references from app.py**

Check `trophydice/app.py` for any import of `socketio` or `sm` and remove those lines. If `python-socketio` is in `pyproject.toml` dependencies, remove it.

- [ ] **Step 3: Remove Socket.IO references from roll handlers**

In `trophydice/handlers/v1/roll.py` and `trophydice/handlers/v2/roll.py`, remove the `from trophydice.socketio import sm` import and any commented-out `await sm.emit(...)` lines.

- [ ] **Step 4: Verify backend starts cleanly**

```bash
python -m uvicorn asgi:app --reload
```

Expected: Backend starts without import errors.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "remove Socket.IO from backend"
```

---

### Task 9: Build and verify production serving

**Files:**
- No new files — verification task

- [ ] **Step 1: Build the frontend**

```bash
cd ui && npx vite build
```

Expected: `ui/dist/` directory created with `index.html`, bundled CSS/JS, and `assets/logo.svg`.

- [ ] **Step 2: Copy build output to FastAPI static directory**

```bash
# Clear old static files and copy new build
find trophydice/static/ -mindepth 1 -delete
cp -r ui/dist/* trophydice/static/
```

- [ ] **Step 3: Test production serving**

Start only the FastAPI backend (no Vite dev server). Navigate to `http://localhost:8000/ui/`. The full app should work — room creation, name input, rolling, polling — all served from FastAPI static files.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "verify production build and static serving"
```

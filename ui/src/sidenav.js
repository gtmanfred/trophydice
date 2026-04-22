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

  const kofi = document.createElement("a");
  kofi.href = "https://ko-fi.com/gtmanfred";
  kofi.target = "_blank";
  kofi.rel = "noopener";
  kofi.className = "btn-kofi";
  kofi.textContent = "Support Me";
  content.appendChild(kofi);
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
  const resetFns = [];

  if (endpoint.method === "GET" && endpoint.params.length > 0) {
    for (const p of endpoint.params) {
      paramValues[p.name] = 0;
      const { row, reset } = buildStepper(p.name, paramValues);
      resetFns.push(reset);
      body.appendChild(row);
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
        if (!selectedColors.includes(c)) {
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
      if (!color || selectedColors.includes(color)) return;
      selectedColors.push(color);
      paramValues[color] = 1;
      const { row, reset } = buildStepper(color, paramValues);
      resetFns.push(reset);
      body.insertBefore(row, colorRow);
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
    if (!roomUid) return;
    rollBtn.disabled = true;
    rollBtn.textContent = "Rolling...";
    try {
      const result = await submitRoll(
        endpoint,
        roomUid,
        getUserName(),
        { ...paramValues }
      );
      if (onRollCallback) onRollCallback(result);
      for (const reset of resetFns) reset();
      closeSidenav();
    } catch {
      rollBtn.classList.add("error");
      rollBtn.textContent = "Failed — tap to retry";
      setTimeout(() => rollBtn.classList.remove("error"), 2000);
    } finally {
      rollBtn.disabled = false;
      if (!rollBtn.classList.contains("error")) rollBtn.textContent = "Roll";
    }
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

  const reset = () => {
    valuesObj[label] = 0;
    display.textContent = "0";
  };

  return { row, reset };
}

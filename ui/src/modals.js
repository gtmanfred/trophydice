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
    if (!name) return;
    currentUser = name;
    nameModal.style.display = "none";
    onReady(getRoomUid());
  }

  saveNameBtn.addEventListener("click", saveName);
  nameInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") saveName();
  });
}

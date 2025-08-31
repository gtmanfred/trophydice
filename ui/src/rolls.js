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
      if (!knownUids.has(roll.uid)) {
        knownUids.add(roll.uid);
        const card = buildRollCard(roll);
        rollList.prepend(card);
      }
    }
    seqId = data.seq_id;
  }
}

export function addRollImmediately(roll) {
  if (!rollList) return;
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

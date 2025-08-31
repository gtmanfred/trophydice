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

// Shared master tables (mt_main_*: employees, cost centers, accounts) live in Mx Data and are owned by TSAT4 SMF.
// They are edited there, never here: saving an account here would drop its admin_of for the other systems.
// So System > Setting in this app shows only the 5S tables (server/modules/act/index.js).
export const MAIN_TABLES = {};

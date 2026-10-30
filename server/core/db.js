import { createClient } from '@supabase/supabase-js';

function db(url, key) {
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
}

// mx = master tables (mt_main_*: employees, cost centers, accounts), tx = 5S tables (mt_5s_*, tx_5s_*).
// Both may point to the same Supabase project (MX_* and TX_* set to the same URL and key). See docs/ARCHITECTURE.md.
export const mx = db(process.env.MX_SUPABASE_URL, process.env.MX_SUPABASE_SECRET_KEY);
export const tx = db(process.env.TX_SUPABASE_URL, process.env.TX_SUPABASE_SECRET_KEY);

export function dbReady() {
  return Boolean(mx && tx && process.env.SESSION_SECRET);
}

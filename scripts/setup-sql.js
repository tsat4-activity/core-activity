// One file to set up an empty Supabase: db/00_main.sql + db/act/5s.sql + db/act/cfo.sql + db/act/smf.sql -> db/setup.sql.
// node scripts/setup-sql.js (npm run test:act checks db/setup.sql is up to date)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (file) => fs.readFileSync(path.join(ROOT, file), 'utf8').replace(/\r\n/g, '\n');

export function setupSql() {
  return `-- TSAT4 Activity: ตั้งฐานข้อมูลใหม่ทั้งหมดในครั้งเดียว = db/00_main.sql + db/act/5s.sql + db/act/cfo.sql + db/act/smf.sql
-- สร้างด้วย node scripts/setup-sql.js ห้ามแก้มือ · รันใน SQL Editor ของ Supabase · รันซ้ำได้

${read('db/00_main.sql')}
${read('db/act/5s.sql')}
${read('db/act/cfo.sql')}
${read('db/act/smf.sql')}`;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  fs.writeFileSync(path.join(ROOT, 'db', 'setup.sql'), setupSql());
  console.log('db/setup.sql written');
}

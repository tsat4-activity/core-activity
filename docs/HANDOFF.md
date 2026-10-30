# HANDOFF — อ่านก่อนเริ่ม และอัปเดตก่อน commit

## กำลังทำอยู่

(ว่าง)

## SQL ที่รอผู้ใช้รัน

- `db/act/cfo.sql` ใน Supabase activity01 (5S + ตารางกลางรันแล้ว) · ฐานว่างใหม่ใช้ `db/setup.sql` ไฟล์เดียว

## ข้อควรระวัง

- `db/setup.sql` สร้างจาก `db/00_main.sql` + `db/act/5s.sql` ด้วย `node scripts/setup-sql.js` ห้ามแก้มือ (`npm run test:act` ตรวจให้)
- `public/app.css` ยังมีสไตล์ของ Store / CFO / Kaizen / QCC ติดมา (ไม่มีผลกับหน้าจอ) ลบทีหลังได้
- ข้อมูลเดิมจาก TSAT4 SMF (พนักงาน, ผลตรวจ 5S, CFO) ยังไม่ได้ย้ายมา · มีไฟล์นำเข้า `inbox/import_5s.sql`, `inbox/import_cfo.sql` (ไม่อยู่ใน git) ทดสอบแล้วใน test:act

## บันทึก (อันใหม่อยู่บนสุด)

- 2026-10-30 · Claude · เพิ่มกิจกรรม SMF (Smart Factory: ทีม ประธาน/รองประธาน/ที่ปรึกษา/Smart Team/ตัวแทนหน่วยงาน + แผนงาน) จาก SMF-act · role `smart` = admin ของ SMF · db/act/smf.sql + setup.sql · **ผู้ใช้ต้องรัน db/act/smf.sql ใน TX (activity01)**

- 2026-10-30 · ปรับปรุงบทบาททีมกิจกรรม 5S ตามข้อกำหนด: ประธาน (`chairman`), รองประธาน (`vice`), ผู้ประสานงาน (`admin`), ผู้ตรวจประเมิน (`auditor`), ผู้รับผิดชอบพื้นที่ (`owner`) ทั้งใน Setting (เพิ่ม/แสดงทีม) และ Dashboard (แท็บ Team)

- 2026-10-30 · Claude · รวม CFO เข้าเว็บเดียวกับ 5S (ชื่อ TSAT4 Activity, โฟลเดอร์ Activity\SMF-5S): cfo.js / act-cfo.js / db/act/cfo.sql จาก SMF-act 8440ac5 · setup.sql รวม cfo · test:act รวม CFO (ข้อมูลจริง tCO2e ตรง Excel) · Setting ไม่แสดง mt_cfo_task (CFO ไม่มี Planner)

- 2026-10-30 · Claude · ใช้ Supabase ของตัวเอง: เพิ่ม `db/00_main.sql` (mt_main_employee / costcenter / user + รหัส 2102899) และ `db/setup.sql` ไฟล์เดียวสำหรับฐานว่าง · ตารางกลางกลับมาแก้ได้ใน System Setting · ทดสอบ ฐานว่าง → setup.sql → bootstrap → login → เพิ่มพนักงาน ผ่าน
- 2026-10-30 · Claude · แยก 5S ออกจาก TSAT4 SMF (commit ต้นทาง 8440ac5): เหลือ login + 5S (Dashboard / Transaction / Setting) + ปฏิทิน + System Setting · ตัด Store, ระบบงาน, CFO, Kaizen, QCC, 100P, SMF, E-DAY, LEAN, SAFETY

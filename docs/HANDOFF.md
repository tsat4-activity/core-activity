# HANDOFF — อ่านก่อนเริ่ม และอัปเดตก่อน commit

## กำลังทำอยู่

(ว่าง)

## SQL ที่รอผู้ใช้รัน

- `db/setup.sql` ใน Supabase โปรเจกต์ใหม่ของ tsat4-activity (ตั้งฐานครั้งแรก: ตารางกลาง + 5S)

## ข้อควรระวัง

- `db/setup.sql` สร้างจาก `db/00_main.sql` + `db/act/5s.sql` ด้วย `node scripts/setup-sql.js` ห้ามแก้มือ (`npm run test:act` ตรวจให้)
- `public/app.css` ยังมีสไตล์ของ Store / CFO / Kaizen / QCC ติดมา (ไม่มีผลกับหน้าจอ) ลบทีหลังได้
- ข้อมูลเดิมจาก TSAT4 SMF (พนักงาน, ผลตรวจ 5S) ยังไม่ได้ย้ายมา

## บันทึก (อันใหม่อยู่บนสุด)

- 2026-10-30 · Claude · ใช้ Supabase ของตัวเอง: เพิ่ม `db/00_main.sql` (mt_main_employee / costcenter / user + รหัส 2102899) และ `db/setup.sql` ไฟล์เดียวสำหรับฐานว่าง · ตารางกลางกลับมาแก้ได้ใน System Setting · ทดสอบ ฐานว่าง → setup.sql → bootstrap → login → เพิ่มพนักงาน ผ่าน
- 2026-10-30 · Claude · แยก 5S ออกจาก TSAT4 SMF (commit ต้นทาง 8440ac5): เหลือ login + 5S (Dashboard / Transaction / Setting) + ปฏิทิน + System Setting · ตัด Store, ระบบงาน, CFO, Kaizen, QCC, 100P, SMF, E-DAY, LEAN, SAFETY

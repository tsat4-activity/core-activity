# HANDOFF — อ่านก่อนเริ่ม และอัปเดตก่อน commit

## กำลังทำอยู่

(ว่าง)

## SQL ที่รอผู้ใช้รัน

ไม่มี · ตาราง 5S อยู่ใน Tx Data แล้ว (สร้างจาก TSAT4 SMF) · ถ้า TSAT4 SMF ยังไม่ได้รัน `db/act/5s_task.sql` (คอลัมน์ `done_on`) และ `db/act/5s_team_roles.sql` (บทบาท `advisor`) ให้รันใน Tx Data ก่อน

## ข้อควรระวัง

- ใช้ Supabase ชุดเดียวกับ TSAT4 SMF: ห้ามแก้ `mt_main_*` และตารางของระบบอื่น · เปลี่ยนโครงตาราง 5S ต้องตกลงกับฝั่ง TSAT4 SMF และแก้ `scripts/act-sql.js` ให้ตรงกันทั้งสอง repo
- cookie ชื่อ `smf_session` แต่คนละโดเมนกับ TSAT4 SMF จึงไม่ปนกัน · `SESSION_SECRET` ของแอปนี้ต้องสุ่มใหม่
- `public/app.css` ยังมีสไตล์ของ Store / CFO / Kaizen / QCC ติดมา (ไม่มีผลกับหน้าจอ) ลบทีหลังได้

## บันทึก (อันใหม่อยู่บนสุด)

- 2026-10-30 · Claude · แยก 5S ออกจาก TSAT4 SMF (commit ต้นทาง 8440ac5): เหลือ login + 5S (Dashboard / Transaction / Setting) + ปฏิทิน + System Setting เฉพาะตาราง 5S · ตัด Store, ระบบงาน, CFO, Kaizen, QCC, 100P, SMF, E-DAY, LEAN, SAFETY · `mt_main_*` ไม่อยู่ใน System Setting (เป็นของ TSAT4 SMF)

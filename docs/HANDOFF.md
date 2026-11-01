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

- 2026-11-01 · Claude · แยกงานให้หลาย AI: `Activity\5S` (branch main) + `Activity\SMF` (git worktree branch smf, inbox = junction ไป 5S) · ตารางว่าใครดูแลไฟล์ไหนอยู่ใน AGENTS.md หัวข้อ 0.1 · `Activity\CFO` เป็นสำเนา CFO แยกเดิม (repo อื่น) ผู้ใช้ให้คงไว้

- 2026-11-01 · Claude · SMF Dashboard แท็บแรก **ภาพรวม** ของโครงการหลัก 5S · CFO · SMF (SMF = Smart Factory ดูแลภาพรวม): KPI รวม + การ์ดต่อโครงการ = ความคืบหน้าแผน (สถานะหัวข้อหลัก) · ผลลัพธ์หลัก (5S คะแนน/ใบตรวจ/Self ค้าง · CFO tCO₂e เทียบปีก่อนเดือนเดียวกัน+เป้า) · ทีม · ปัญหา (Issue / แผนเลยกำหนด) · API `GET /api/act/overview` (server/modules/act/overview.js) อ่านอย่างเดียว ตารางที่ยังไม่สร้าง = ส่วนนั้นว่าง

- 2026-10-30 · Claude · ทีม (5S / CFO / SMF ใช้ a5SetTeam ร่วมกัน) เพิ่มปุ่มแก้ไข: เปลี่ยนทีม บทบาท กลุ่มตรวจ พื้นที่ หน่วยงาน สถานะ (PATCH /team/:id ตรวจแบบเดียวกับเพิ่ม `placementOf`) · ตรวจทุกหน้าแล้ว หน้าอื่นมี เพิ่ม/แก้ไข/ลบ ครบ · กฎใหม่ใน AGENTS.md

- 2026-10-30 · Claude · โครงสร้างทีมใหม่ทุกกิจกรรม (docs/specs/act-teams.md): เริ่มด้วย ประธาน · รองประธาน · ที่ปรึกษา · ผู้ประสานงาน · 5S มีคอลัมน์ `unit` = 4 ทีมย่อย (มาตรฐาน / วิชาการ / ประชาสัมพันธ์ / ตรวจประเมิน) แทนร่าง role standard/academic/pr (ย้ายข้อมูลให้เอง) · Issue เมื่อคะแนน**ต่ำกว่า** 3 · Action ก่อนตรวจถัดไป 15 วัน · ปิด Issue เมื่อตรวจได้ ≥ 3 · **ผู้ใช้ต้องรัน db/act/5s.sql, cfo.sql, smf.sql ซ้ำใน TX (activity01)**

- 2026-10-30 · Claude · `mt_main_employee.photo` รูปพนักงาน 2.5:3: Setting เลือกรูป → ครอป 500×600 JPEG ในเบราว์เซอร์ (`cropJpeg` แทน squareJpeg ที่ไม่มีใครใช้) → server อัปโหลด Storage `img_main` ของ MX แล้วเก็บลิงก์ · ติ๊ก ลบรูป = ล้างค่า (ไฟล์เก่าไม่ลบ) · **ผู้ใช้ต้องรัน db/00_main.sql ซ้ำใน MX (activity02)**

- 2026-10-30 · จัดโครงสร้าง Table 5S ครบ 3 ส่วน:
  1. **ทีม:** ทีมบริหาร (`chairman`, `vice`, `admin` ผู้ประสานงาน) แยกโครงสร้างย่อยเป็นทีมมาตรฐาน (`standard`), ทีมวิชาการ (`academic`), ทีมตรวจประเมิน (`auditor` ทีม A–Z), ทีมประชาสัมพันธ์ (`pr`)
  2. **พื้นที่ประเมิน:** ผู้รับผิดชอบพื้นที่ (`owner`) เป็นผู้ดูแลพื้นที่
  3. **หัวข้อประเมิน:** ร่างหัวข้อมาตรฐาน 25 ข้อ (ส1–ส5 หมวดละ 5 ข้อ เต็ม 125) ใน `db/act/5s.sql`, `db/setup.sql` และ `db/act/5s_checklist_seed.sql` รันซ้ำได้

- 2026-10-30 · Claude · เพิ่มกิจกรรม SMF (Smart Factory: ทีม ประธาน/รองประธาน/ที่ปรึกษา/Smart Team/ตัวแทนหน่วยงาน + แผนงาน) จาก SMF-act · role `smart` = admin ของ SMF · db/act/smf.sql + setup.sql · **ผู้ใช้ต้องรัน db/act/smf.sql ใน TX (activity01)**

- 2026-10-30 · ปรับปรุงบทบาททีมกิจกรรม 5S ตามข้อกำหนด: ประธาน (`chairman`), รองประธาน (`vice`), ผู้ประสานงาน (`admin`), ผู้ตรวจประเมิน (`auditor`), ผู้รับผิดชอบพื้นที่ (`owner`) ทั้งใน Setting (เพิ่ม/แสดงทีม) และ Dashboard (แท็บ Team)

- 2026-10-30 · Claude · รวม CFO เข้าเว็บเดียวกับ 5S (ชื่อ TSAT4 Activity, โฟลเดอร์ Activity\SMF-5S): cfo.js / act-cfo.js / db/act/cfo.sql จาก SMF-act 8440ac5 · setup.sql รวม cfo · test:act รวม CFO (ข้อมูลจริง tCO2e ตรง Excel) · Setting ไม่แสดง mt_cfo_task (CFO ไม่มี Planner)

- 2026-10-30 · Claude · ใช้ Supabase ของตัวเอง: เพิ่ม `db/00_main.sql` (mt_main_employee / costcenter / user + รหัส 2102899) และ `db/setup.sql` ไฟล์เดียวสำหรับฐานว่าง · ตารางกลางกลับมาแก้ได้ใน System Setting · ทดสอบ ฐานว่าง → setup.sql → bootstrap → login → เพิ่มพนักงาน ผ่าน
- 2026-10-30 · Claude · แยก 5S ออกจาก TSAT4 SMF (commit ต้นทาง 8440ac5): เหลือ login + 5S (Dashboard / Transaction / Setting) + ปฏิทิน + System Setting · ตัด Store, ระบบงาน, CFO, Kaizen, QCC, 100P, SMF, E-DAY, LEAN, SAFETY

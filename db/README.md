# db/ — SQL ที่รันเองใน Supabase

AI ไม่มีสิทธิ์เข้าฐานข้อมูล ผู้ใช้รันไฟล์ใน SQL Editor ของ Supabase เอง

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `setup.sql` | **ฐานว่าง รันไฟล์นี้ไฟล์เดียว** = `00_main.sql` + `act/5s.sql` (สร้างด้วย `node scripts/setup-sql.js` ห้ามแก้มือ) รันซ้ำได้ |
| `00_main.sql` | ตารางกลาง `mt_main_employee`, `mt_main_costcenter`, `mt_main_user` + รหัสผู้ดูแลแรก 2102899 |
| `act/5s.sql` | ตาราง 5S ทั้งชุด + bucket `img_5s` สร้างจาก `scripts/act-sql.js` เท่านั้น ห้ามแก้มือ |
| `act/5s_task.sql` | สำหรับฐาน 5S เก่าที่ยังไม่มี Project Planner (ฐานใหม่ไม่ต้องใช้) |
| `act/5s_team_roles.sql` | สำหรับฐาน 5S เก่าที่ยังไม่มีบทบาท `advisor` (ฐานใหม่ไม่ต้องใช้) |

เปลี่ยนแม่แบบ: แก้ `scripts/act-sql.js` → `node scripts/act-sql.js 5s` → `node scripts/setup-sql.js` → `npm run test:act`

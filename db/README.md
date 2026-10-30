# db/ — SQL ของตาราง 5S (อ้างอิง)

ตารางทั้งหมดสร้างไว้แล้วใน **Tx Data** ซึ่งใช้ร่วมกับ TSAT4 SMF ไม่ต้องรันซ้ำ · AI ไม่มีสิทธิ์เข้าฐานข้อมูล ผู้ใช้รันเองใน SQL Editor

| ไฟล์ | ฐาน | ใช้ทำอะไร |
|---|---|---|
| `act/5s.sql` | **Tx Data** | ตาราง 5S ทั้งชุด สร้างจาก `scripts/act-sql.js` เท่านั้น ห้ามแก้มือ รันซ้ำได้ |
| `act/5s_task.sql` | **Tx Data** | เพิ่ม Project Planner (`mt_5s_task` + `done_on`) และคัดลอกแผน Gantt เดิมครั้งเดียว |
| `act/5s_team_roles.sql` | **Tx Data** | บทบาท `advisor` (ที่ปรึกษา) ใน `mt_5s_team` · รันซ้ำได้ |

เปลี่ยนแม่แบบ: แก้ `scripts/act-sql.js` → `node scripts/act-sql.js 5s` → `npm run test:act` · **ตกลงกับฝั่ง TSAT4 SMF ก่อน** เพราะใช้ตารางเดียวกัน

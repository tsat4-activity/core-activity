# SMF — Smart Factory

ผู้ใช้กำหนด 2026-10-29: SMF = **Smart Factory** · สถานะ: ทีมทำแล้ว (ผู้ใช้ยืนยัน 2026-10-29) · ข้อ 1–3 ด้านล่าง Claude เลือกค่าตั้งต้นให้ ผู้ใช้เปลี่ยนได้
ตาราง: `db/act/smf.sql` (`node scripts/act-sql.js smf --no-audit`) · ตอนนี้มีแค่ทีม + แผนงาน (Project Planner, `docs/specs/act-planner.md`)

## ทีม (`mt_smf_team`)

ลำดับตามที่ผู้ใช้ให้มา:

| ลำดับ | ชื่อบนจอ | role ที่เสนอ | มีอยู่แล้ว? | หมายเหตุ |
|---|---|---|---|---|
| 1 | ประธาน | `chairman` | มี | อนุมัติ / ดูทุกหน้า (เหมือนกิจกรรมอื่น) |
| 2 | รองประธาน | `vice` | มี | สิทธิ์เท่าประธาน |
| 3 | ที่ปรึกษา | `advisor` | กำลังเพิ่ม (Antigravity 2026-10-29: แม่แบบ role check + `accessOf().advisor`) | ดูได้ทุกหน้า · ยังไม่ได้กำหนดว่าอนุมัติได้หรือไม่ |
| 4 | Smart Team | `smart` (ใหม่) | ยังไม่มี | ทีมทำงานหลักของ Smart Factory · ต้องเพิ่มใน role check ของแม่แบบ + `ROLES` (server/modules/act/audit.js) |
| 5 | ตัวแทนหน่วยงาน | `member` + `department` | มี | 1 คนต่อหน่วยงาน (กฎเดิม: member ต้องมีหน่วยงาน) |

ป้ายบนจอของ SMF เป็นชุดเฉพาะของ SMF (ผู้ใช้ 2026-10-29: โครงสร้างทีมแต่ละกิจกรรมไม่เหมือนกัน) · ภาพรวมทุกกิจกรรม: `act-teams.md`

## ค่าที่เลือกให้ (เปลี่ยนได้) และคำถามที่ยังเปิด

ค่าที่ใช้ตอนนี้: Smart Team (`smart`) = สิทธิ์ admin ดูแล Setting (ทีม + แผนงาน) · ที่ปรึกษา (`advisor`) ดูอย่างเดียว · Smart Team เป็นรายชื่อเดียว ไม่แบ่งทีมย่อย · ผู้ดูแลระบบภาพรวม (creator / admin_of smf) ยังแก้ได้เสมอ


1. **ใครดูแล Setting ของ SMF** (สิทธิ์ `admin` เพิ่ม/แก้ทีม แผนงาน): รายชื่อทีมไม่มี "เลขา" · ให้ Smart Team เป็นผู้ดูแล (`smart` มีสิทธิ์ admin) หรือยังมีเลขาแยก
2. **ที่ปรึกษา** อนุมัติ / แก้ข้อมูลได้ไหม หรือดูอย่างเดียว
3. **Smart Team** มีหลายคน แบ่งเป็นทีมย่อย (เช่น ทีม A / B แบบผู้ตรวจ 5S) หรือรายชื่อเดียว
4. SMF มีงานอะไรนอกจากแผนงาน (เช่น ทะเบียนโครงการ Smart Factory, KPI, ระดับความพร้อม) — Transaction / Dashboard ยังว่าง

## ที่ต้องแก้เมื่อยืนยัน (ไม่ต้องรัน SQL ใหม่ถ้าใช้แค่ role ที่มี)

- `scripts/act-sql.js` role check: เพิ่ม `smart` → สร้าง `db/act/*.sql` ใหม่ → **ผู้ใช้รัน `db/act/smf.sql` ใน Tx Data**
- `server/modules/act/audit.js` `ROLES` + `server/modules/act/common.js` `accessOf` (สิทธิ์ของ advisor / smart)
- `public/js/act-planner.js` ป้ายบทบาทของ SMF (`APL_ROLE_LABEL` แยกตามกิจกรรม) + หน้า Dashboard > Team
- `public/js/units.js` ชื่อ SMF แสดง "SMF · Smart Factory"

## Dashboard > ภาพรวม · หน้าหลัก (ผู้ใช้กำหนด 2026-11-01)

- **SMF Dashboard > ภาพรวม** = เฉพาะ SMF: KPI (ความคืบหน้ารวม · โครงการปีนี้ · หัวข้อเลยกำหนด · คนในทีม) + การ์ดต่อโครงการ (ความคืบหน้า · สถานะหัวข้อหลัก · เลยกำหนด · ทีมโครงการ) · `aplDrawSmfOverview`
- **หน้าหลัก** = ภาพรวมกิจกรรมในโรงงาน 5S · CFO · SMF (การ์ดต่อกิจกรรม + ปุ่มเปิด Dashboard) · `aplHome` / `aplDrawOverview` · API `GET /api/act/overview?year=` (`server/modules/act/overview.js`)

## โครงการรายปี (ผู้ใช้กำหนด 2026-11-01)

SMF = กิจกรรม Smart Factory ในโรงงาน (คู่กับ 5S = กิจกรรม 5ส, CFO = Carbon Footprint) · ปี 2026 มี 3 โครงการ: **Smart OEE** (`oee`) · **Vision Camera** (`vision`) · **Work Flow Automation** (`workflow`)
- ตาราง `mt_smf_project` (year, code, name, sort_no, status) · Setting > โครงการ: เพิ่ม / แก้ไข / ลบ / คัดลอกจากปีก่อน (เฉพาะ Active) · มีทีมหรือแผนแล้ว ลบ = Inactive และเปลี่ยนรหัสไม่ได้ (`server/modules/act/smf.js`)
- **ทีม**: คณะกรรมการ SMF (unit ว่าง: ประธาน · รองประธาน · ที่ปรึกษา · ผู้ประสานงาน · Smart Team · ตัวแทนหน่วยงาน) + ทีมของแต่ละโครงการ (`mt_smf_team.unit` = code: ประธาน · รองประธาน · ที่ปรึกษา · ผู้ประสานงาน · สมาชิก)
- **แผนงาน**: ข้อหลักเลือกโครงการ (`mt_smf_task.unit`) ข้อรองตามข้อหลัก · Gantt จัดกลุ่มตามโครงการ + ตัวกรอง โครงการ
- **Dashboard**: ภาพรวมแสดงต่อโครงการ (ความคืบหน้า · หัวข้อ · เลยกำหนด · ทีม) · Team แยกการ์ดต่อโครงการ

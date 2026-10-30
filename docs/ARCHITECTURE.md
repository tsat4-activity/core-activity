# โครงสร้าง TSAT4 5S

เว็บแอปเดียว: Node 22 + Express ต่อกับ Supabase 2 ก้อน (ชุดเดียวกับ TSAT4 SMF) frontend เป็น vanilla JS ไม่มีขั้นตอน build

| ฐาน | client / env | ใช้อะไร |
|---|---|---|
| **Mx Data** (ezhyitqznflvjnwuuchn) | `mx` / `MX_SUPABASE_*` | อ่าน `mt_main_employee`, `mt_main_costcenter`, `mt_main_user` (login) · เขียนได้แค่รหัสผ่านของตัวเอง · เจ้าของคือ TSAT4 SMF |
| **Tx Data** (loeyrgavlpdnrbczjxpl) | `tx` / `TX_SUPABASE_*` | ตาราง 5S `mt_5s_*` / `tx_5s_*` / `v_5s_*` และที่เก็บรูป `img_5s` (สร้างจาก scripts/act-sql.js) |

ชื่อพนักงานในหน้า 5S ดึงจาก Mx Data แยกอีกครั้ง (`namesOf`) เพราะคนละฐาน
deploy บน Render (`render.yaml`): push ไปที่ `main` แล้ว deploy อัตโนมัติ

```
server.js                    จุดเริ่ม: createApp().listen() + bootstrap
server/
  app.js                     ประกอบแอป: auth → ทุกโมดูลใน MODULES → static → fallback index.html
  core/
    db.js                    mx = Mx Data (master, อ่าน) / tx = Tx Data (5S)
    http.js                  fail, wrap, cleanTerm, adminWriteError
    session.js               cookie smf_session (HMAC, อายุ 7 วัน)
    access.js                CREATOR_ID, ADMIN_SCOPES ['5s'], defineModule, atLeast, creatorOnly
    users.js                 loadUser, publicUser, requireUser (รหัสผ่านหมดอายุทุก 90 วัน)
    auth.js                  /api/health, login, logout, me, password, bootstrap
    tables.js                MAIN_TABLES = {} (mt_main_* แก้ที่ TSAT4 SMF)
  modules/
    index.js                 MODULES = [act, system]
    act/index.js             ปฏิทิน /api/act/calendar + ตาราง 5S ใน System Setting + รวม route
    act/common.js            tablesOf('5s') ชื่อตาราง, actRoute (ตารางยังไม่มี → 503), accessOf (สิทธิ์รายปีจาก mt_5s_team), fetchAll/fetchIn, namesOf
    act/audit.js             Dashboard + Setting (พื้นที่ / ทีม / หัวข้อ / แผนตรวจ) summarize()/rank()
    act/transaction.js       บันทึกผลตรวจ Self/Committee + Issue (รูปใน bucket img_5s)
    act/planner.js           Project Planner /api/act/5s/tasks (mt_5s_task) spec docs/specs/act-planner.md
    system/index.js          /api/system/tables (เฉพาะ creator) เฉพาะตาราง 5S
public/
  index.html                 โครงหน้า + sidebar + ลำดับ <script>
  app.css
  js/core.js                 helper, popup, api(), login, router (VIEWS / TITLES / ACCESS), กราฟ, ตาราง
  js/units.js                ACTIVITIES = 5S + เมนู
  js/act.js                  ปฏิทิน (สัปดาห์ / เดือน / ปี) + helper วันที่
  js/act-5s.js               5S > Dashboard (Summary/Ranking/Schedule/Audit Plan/Team) + Setting (ทีม/แผนงาน/พื้นที่/หัวข้อตรวจ/แผนตรวจ)
  js/act-tx.js               5S > Transaction: ใบตรวจ + ฟอร์มตรวจ + Issue
  js/act-planner.js          Project Planner รายปี (W1–W4) / รายเดือน ลากแท่งได้
  js/system.js               หน้าแก้ตาราง 5S ของ creator
  js/boot.js                 bind event, สร้าง sidebar, โหลด session (ต้องอยู่ท้ายสุด)
db/act/                      SQL ตาราง 5S (อ้างอิง สร้างไว้แล้วใน Tx Data)
scripts/
  act-sql.js                 แม่แบบตารางกิจกรรม (ต้องตรงกับ TSAT4 SMF)
  check.js                   npm run check
  test-act-audit.js          npm run test:act
  routes.snapshot.txt        รายการ route + สิทธิ์ที่ถูกต้อง
```

## สิทธิ์

- `creator` (mt_main_user) ทำได้ทุกอย่าง และเปิด System Setting ได้
- ผู้ดูแล 5S ทุกปี: `admin_of` มี `5s` (ตั้งที่ TSAT4 SMF) · `executive` = ประธานทุกปี
- รายปีจาก `mt_5s_team`: `admin` (เลขา) = Setting และแผน · `chairman` / `vice` / `auditor` / เจ้าของพื้นที่ (`owner` + area_id) = Transaction · ทุกคนที่ login = Dashboard
- route เขียนข้อมูลตรวจ admin ของปีนั้นใน handler snapshot จึงแสดงแค่ `auth`

## ตารางที่ใช้

| ตาราง | db | หน้าที่ |
|---|---|---|
| mt_main_employee / _costcenter / _user | mx | พนักงาน, หน่วยงาน, บัญชี login (อ่านอย่างเดียว) |
| mt_5s_team / _area / _checklist / _audit_plan / _setting / _task | tx | ทีมรายปี (รวมเจ้าของพื้นที่), พื้นที่, หัวข้อตรวจรายปี, แผนตรวจ, ค่าตั้งต้น, Project Planner |
| tx_5s_audit (+ auditors, receivers) / _audit_score / _issue, v_5s_audit_group | tx | ผลตรวจ คะแนนรายข้อ Issue และ % ราย ส |

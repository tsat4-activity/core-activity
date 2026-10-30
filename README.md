# TSAT4 Activity

ระบบกิจกรรมเว็บเดียว: **5S** (Dashboard · ตรวจพื้นที่และ Issue · ทีม · แผนงาน · พื้นที่ · Checklist · แผนตรวจ) และ **CFO** (Carbon Footprint for Organization: Dashboard · บันทึกรายเดือน · Fr-01 – Fr-04.1) และ **SMF** (Smart Factory: ทีม + แผนงาน) + ปฏิทินรวม
แยกออกมาจาก TSAT4 SMF เมื่อ 2026-10-30 · มี Render และ Supabase ของตัวเอง

## เทคโนโลยี

- Node.js 22 + Express 4 (ES modules) · หน้าเว็บ HTML + CSS + JavaScript ธรรมดา
- Supabase ผ่าน `@supabase/supabase-js` ฝั่งเซิร์ฟเวอร์เท่านั้น
- Render (Web Service) deploy อัตโนมัติเมื่อ push ขึ้น `main`

## ติดตั้งครั้งแรก

### 1. Supabase

1. สร้างโปรเจกต์ใหม่ใน Supabase
2. เปิด **SQL Editor → New query** วางเนื้อหาไฟล์ `db/setup.sql` ทั้งไฟล์ แล้วกด **Run** (รันซ้ำได้)
3. **Project Settings → API Keys** จด Project URL และ secret key ไว้ใส่ใน Render (ห้ามส่งในแชทหรือใส่ใน git)

### 2. Render

1. New → Web Service → เลือก repo นี้ (หรือ New → Blueprint ใช้ `render.yaml`)
2. Build `npm install` · Start `npm start`
3. Environment (ดู `.env.example`):
   - `NODE_VERSION` = `22`
   - `MX_SUPABASE_URL` และ `TX_SUPABASE_URL` = Project URL (ค่าเดียวกัน)
   - `MX_SUPABASE_SECRET_KEY` และ `TX_SUPABASE_SECRET_KEY` = secret key (ค่าเดียวกัน)
   - `SESSION_SECRET` = ข้อความสุ่มยาว ๆ
   - `BOOTSTRAP_EMPLOYEE_ID` = `2102899` และ `BOOTSTRAP_PASSWORD` = รหัสผ่านแรก (อย่างน้อย 8 ตัว)
4. เปิด `/api/health` ต้องได้ `{"ok":true,"database":true}`
5. login ด้วย `2102899` + รหัสผ่านแรก → Setting → `mt_main_employee` แก้ชื่อตัวเอง แล้วเพิ่มหน่วยงาน (`mt_main_costcenter`) พนักงาน และบัญชี (`mt_main_user`)
6. หลัง login ได้แล้ว ลบ `BOOTSTRAP_PASSWORD` ออกจาก Render ได้

### 3. ตั้งค่ากิจกรรม

- 5S → Setting: ทีม (ผู้ประสานงาน = ผู้ดูแลปีนั้น) → แผนงาน → พื้นที่ → หัวข้อตรวจ → แผนตรวจ
- CFO → Setting: ทีม → บริษัท (Fr-01) → EF / กิจกรรมรายหน่วยงาน
- SMF → Setting: ทีม (Smart Team = ผู้ดูแล) → แผนงาน

## พัฒนา

```
npm install
npm run check      # ตรวจ syntax, route, เปิดเซิร์ฟเวอร์
npm run test:act   # ทดสอบ db/setup.sql และตาราง 5S / CFO บน Postgres จำลอง
npm start
```

กฎการทำงานอยู่ใน `AGENTS.md` · สถานะล่าสุดใน `docs/HANDOFF.md`

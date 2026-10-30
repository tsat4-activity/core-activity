# TSAT4 5S

ระบบกิจกรรม 5S (Dashboard · ตรวจพื้นที่และ Issue · ทีม · แผนงาน · พื้นที่ · Checklist · แผนตรวจ · ปฏิทิน)
แยกออกมาจาก TSAT4 SMF เมื่อ 2026-10-30 · ใช้ Supabase ชุดเดียวกับ TSAT4 SMF ข้อมูล 5S จึงเห็นตรงกันทั้งสองแอป

## เทคโนโลยี

- Node.js 22 + Express 4 (ES modules) · หน้าเว็บ HTML + CSS + JavaScript ธรรมดา
- Supabase ผ่าน `@supabase/supabase-js` ฝั่งเซิร์ฟเวอร์เท่านั้น
- Render (Web Service) deploy อัตโนมัติเมื่อ push ขึ้น `main`

## ติดตั้งบน Render

1. New → Web Service → เลือก repo นี้ (หรือ New → Blueprint ใช้ `render.yaml`)
2. Build `npm install` · Start `npm start` · Environment `NODE_VERSION=22`
3. ใส่ Environment ตาม `.env.example` (ค่าเดียวกับ TSAT4 SMF ยกเว้น `SESSION_SECRET` ให้สุ่มใหม่):
   `MX_SUPABASE_URL`, `MX_SUPABASE_SECRET_KEY`, `TX_SUPABASE_URL`, `TX_SUPABASE_SECRET_KEY`, `SESSION_SECRET`
4. เปิด `/api/health` ต้องได้ `{"ok":true,"database":true}`

ไม่ต้องรัน SQL เพิ่ม ตาราง 5S มีอยู่แล้วใน Tx Data (`db/act/5s*.sql` เก็บไว้อ้างอิง)

## ข้อมูลที่เป็นของ TSAT4 SMF

พนักงาน, costcenter และบัญชีเข้าสู่ระบบ (`mt_main_*` ใน Mx Data) แก้ที่ TSAT4 SMF เท่านั้น แอปนี้อ่านอย่างเดียว
ให้ใครเป็นผู้ดูแล 5S ทุกปี: TSAT4 SMF > Setting > `mt_main_user` > ผู้ดูแลระบบ ติ๊ก 5S · หรือใส่เป็น เลขา ในทีม 5S ของปีนั้น

## พัฒนา

```
npm install
npm run check      # ตรวจ syntax, route, เปิดเซิร์ฟเวอร์
npm run test:act   # ทดสอบตาราง 5S บน Postgres จำลอง
npm start
```

กฎการทำงานอยู่ใน `AGENTS.md` · สถานะล่าสุดใน `docs/HANDOFF.md`

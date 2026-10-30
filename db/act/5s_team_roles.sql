-- 5S: จัดโครงสร้างทีมใหม่ เพิ่มบทบาททีมย่อย (standard = ทีมมาตรฐาน, academic = ทีมวิชาการ, pr = ทีมประชาสัมพันธ์) ใน mt_5s_team
-- รันใน Tx Data ของ Supabase · รันซ้ำได้
alter table public.mt_5s_team
  drop constraint if exists mt_5s_team_role_check,
  add constraint mt_5s_team_role_check check (role in ('admin', 'chairman', 'vice', 'advisor', 'smart', 'auditor', 'owner', 'member', 'standard', 'academic', 'pr'));

notify pgrst, 'reload schema';

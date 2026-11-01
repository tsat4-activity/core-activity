import { tx } from '../../core/db.js';
import { fail } from '../../core/http.js';
import { PROJECT_ON, actRoute, must, projectsOf, requireAdmin, tablesOf, yearOf } from './common.js';

// SMF (Smart Factory) projects of a year (ผู้ใช้กำหนด 2026-11-01: 2026 = Smart OEE, Vision Camera, Work Flow Automation).
// Setting > โครงการ: admins add / edit / delete; a project already used by the team or the plan becomes Inactive instead.
// The code is what mt_smf_team.unit and mt_smf_task.unit point at, so it cannot change once used.
const CODE = /^[a-z0-9_-]{1,20}$/;

export function mountSmf(app) {
  const route = actRoute(app, { only: PROJECT_ON });
  const usedBy = async (t, project) => {
    const [team, task] = await Promise.all([
      tx.from(t.team).select('id', { count: 'exact', head: true }).eq('year', project.year).eq('unit', project.code),
      tx.from(t.task).select('id', { count: 'exact', head: true }).eq('year', project.year).eq('unit', project.code)
    ]);
    if (team.error || task.error) throw team.error || task.error;
    return (team.count || 0) + (task.count || 0);
  };
  const input = (body) => {
    const name = String(body?.name || '').trim().slice(0, 120);
    const code = String(body?.code || '').trim().toLowerCase();
    if (!name) return { error: 'ระบุชื่อโครงการ' };
    if (!CODE.test(code)) return { error: 'รหัสใช้ a–z 0–9 - _ ไม่เกิน 20 ตัว เช่น oee' };
    const sort = Number(body?.sortNo);
    return { row: { name, code, sort_no: Number.isInteger(sort) && sort > 0 ? sort : 1, status: body?.status === 'Inactive' ? 'Inactive' : 'Active' } };
  };

  route('get', '/api/act/:activity/projects', async (req, res, activity) => {
    const year = yearOf(req.query.year);
    if (!year) return fail(res, 400, 'ปีไม่ถูกต้อง');
    res.json({ year, projects: await projectsOf(activity, year) });
  });

  route('post', '/api/act/:activity/projects', async (req, res, activity, t) => {
    const year = yearOf(req.body?.year);
    if (!year || !(await requireAdmin(req, res, activity, year))) return;
    const { row, error } = input(req.body);
    if (error) return fail(res, 400, error);
    const done = await tx.from(t.project).insert({ ...row, year });
    if (done.error?.code === '23505') return fail(res, 400, `ปี ${year} มีรหัส ${row.code} แล้ว`);
    must(done);
    res.status(201).json({ ok: true });
  });

  route('patch', '/api/act/:activity/projects/:id', async (req, res, activity, t) => {
    const project = must(await tx.from(t.project).select('*').eq('id', Number(req.params.id)).maybeSingle());
    if (!project) return fail(res, 404, 'ไม่พบโครงการ');
    if (!(await requireAdmin(req, res, activity, project.year))) return;
    const { row, error } = input({ code: project.code, ...req.body });
    if (error) return fail(res, 400, error);
    if (row.code !== project.code && await usedBy(t, project)) return fail(res, 400, 'โครงการนี้มีทีม / แผนงานแล้ว เปลี่ยนรหัสไม่ได้');
    const done = await tx.from(t.project).update(row).eq('id', project.id);
    if (done.error?.code === '23505') return fail(res, 400, `ปี ${project.year} มีรหัส ${row.code} แล้ว`);
    must(done);
    res.json({ ok: true });
  });

  route('delete', '/api/act/:activity/projects/:id', async (req, res, activity, t) => {
    const project = must(await tx.from(t.project).select('*').eq('id', Number(req.params.id)).maybeSingle());
    if (!project) return fail(res, 404, 'ไม่พบโครงการ');
    if (!(await requireAdmin(req, res, activity, project.year))) return;
    if (await usedBy(t, project)) {
      must(await tx.from(t.project).update({ status: 'Inactive' }).eq('id', project.id));
      return res.json({ ok: true, inactive: true });
    }
    must(await tx.from(t.project).delete().eq('id', project.id));
    res.json({ ok: true });
  });

  // Next year: copy the Active projects (codes and names) from another year; existing codes are kept.
  route('post', '/api/act/:activity/projects/copy', async (req, res, activity, t) => {
    const from = yearOf(req.body?.from);
    const to = yearOf(req.body?.to);
    if (!from || !to || from === to) return fail(res, 400, 'เลือกปีต้นทางและปลายทาง');
    if (!(await requireAdmin(req, res, activity, to))) return;
    const rows = (await projectsOf(activity, from)).filter((p) => p.status === 'Active');
    if (!rows.length) return fail(res, 400, `ปี ${from} ไม่มีโครงการ Active ให้คัดลอก`);
    const done = await tx.from(tablesOf(activity).project).upsert(rows.map(({ code, name, sort_no, status }) => ({ year: to, code, name, sort_no, status })), { onConflict: 'year,code', ignoreDuplicates: true });
    must(done);
    res.json({ ok: true, copied: rows.length });
  });
}

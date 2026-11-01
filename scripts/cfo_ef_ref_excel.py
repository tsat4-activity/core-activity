"""EF reference tables of CFO from the TGO workbook -> db/act/cfo_ef_ref_seed.sql (mt_cfo_ef_ref + GWP AR5).

    python -I scripts/cfo_ef_ref_excel.py "C:/Work/projects/Store/inbox/Verify sheet TGO.xlsx"

Sheet "EF TGO AR5 V2": GWP (row 8), EF for energy consumption per unit (rows 15-159), common chemical GWP
(rows 164-175) and EF from IPCC Guidelines per TJ (rows 188-234). The seed fills a table only while it is empty,
so rows edited in Setting > Emission Factor are never overwritten. spec: docs/specs/act-cfo.md
"""
import sys
import warnings
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
SHEETS = [('energy', 15, 159), ('chemical', 164, 175), ('ipcc', 188, 234)]
NUMERIC = {c: 'numeric' for c in ('co2', 'ch4_fossil', 'ch4', 'n2o', 'total', 'ratio')} | {'sort_no': 'integer'}


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def txt(v):
    if v is None:
        return None
    s = ' '.join(str(v).split())
    return s or None


def lit(v):
    if v is None:
        return 'null'
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f'{v:.12g}'  # 12 digits: drops float noise (1.0200000000000001e-07)
    if isinstance(v, int):
        return str(v)
    return "'" + v.replace("'", "''") + "'"


def main(book_path):
    warnings.simplefilter('ignore')
    ws = openpyxl.load_workbook(book_path, read_only=True, data_only=True)['EF TGO AR5 V2']
    rows = {i: r for i, r in enumerate(ws.iter_rows(min_row=1, max_row=240, values_only=True), start=1)}
    g = rows[8]
    out = ['-- CFO: ตารางอ้างอิง Emission Factor (แผ่น EF TGO AR5 V2) · สร้างจาก scripts/cfo_ef_ref_excel.py ห้ามแก้มือ',
           '-- รันใน Tx Data หลัง db/act/cfo.sql · รันซ้ำได้: เติมเฉพาะตารางที่ยังว่าง ไม่ทับค่าที่แก้ใน Setting', '',
           'insert into public.mt_cfo_gwp (code, co2, ch4_fossil, ch4, n2o, sf6, nf3, reference) values',
           f"  ('AR5', {g[2]}, {g[3]}, {g[4]}, {g[5]}, 23500, 16100, {lit(txt(rows[7][6]).replace('Ref.: ', ''))})",
           'on conflict (code) do nothing;', '']
    cols = ['sheet', 'grp', 'name', 'formula', 'unit', 'co2', 'ch4_fossil', 'ch4', 'n2o', 'total', 'ratio', 'reference', 'remark', 'sort_no']
    for sheet, first, last in SHEETS:
        values, grp = [], None
        for i in range(first, last + 1):
            r = rows[i]
            name = txt(r[2])
            if not name:
                continue
            grp = txt(r[1]) or grp
            gas = [num(r[k]) for k in (5, 6, 7, 8)]
            total = num(r[9])
            unit = txt(r[4])
            if sheet == 'ipcc':
                unit = 'TJ' if gas[0] is not None else None
            if not unit and all(v is None for v in gas):
                total = None  # heading row (e.g. On-road vehicles)
            remark = ' · '.join(x for x in (txt(r[13]), txt(r[14])) if x) or None
            values.append([sheet, grp, name, None, unit, *gas, total, num(r[12]), txt(r[10]), remark, len(values) + 1])
        out.append(f'-- {sheet}: {len(values)} แถว')
        out.append(f'insert into public.mt_cfo_ef_ref ({", ".join(cols)})')
        picks = ', '.join(f'v.{c}::{NUMERIC.get(c, "text")}' for c in cols)
        out.append(f'select {picks} from (values')
        out.append(',\n'.join('  (' + ', '.join(lit(v) for v in row) + ')' for row in values))
        out.append(f') as v ({", ".join(cols)})')
        out.append(f"where not exists (select 1 from public.mt_cfo_ef_ref where sheet = '{sheet}');")
        out.append('')
    target = ROOT / 'db' / 'act' / 'cfo_ef_ref_seed.sql'
    target.write_text('\n'.join(out), encoding='utf-8', newline='\n')
    print(f'{target.relative_to(ROOT)} written')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'inbox' / 'Verify sheet TGO.xlsx')

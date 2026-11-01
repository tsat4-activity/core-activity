"""SAP materials (Store usage list) -> inbox/import_cfo_material.sql for mt_cfo_material (CFO Scope 3 วัสดุ).

    python -I scripts/import_cfo_material.py "C:/Work/projects/Store/inbox/master_sto.xlsx"

Sheet "usage": no · material · material_description · bun (SAP unit) · price · crcy · status. Only the list is loaded;
the EF and the unit factor are matched later in Setting > วัสดุ (SAP). Re-running keeps that matching (on conflict
updates name / unit / price only). The file stays in inbox/ (company data, not in git). spec: docs/specs/act-cfo.md
"""
import sys
import warnings
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent


def lit(v):
    if v is None:
        return 'null'
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return str(int(v)) if float(v).is_integer() else repr(float(v))
    return "'" + str(v).replace("'", "''") + "'"


def main(book_path):
    warnings.simplefilter('ignore')
    ws = openpyxl.load_workbook(book_path, read_only=True, data_only=True)['usage']
    rows = ws.iter_rows(values_only=True)
    head = [str(h or '').strip().lower() for h in next(rows)]
    col = {name: head.index(name) for name in ('material', 'material_description', 'bun', 'price', 'status')}
    seen, values = set(), []
    for r in rows:
        code = str(r[col['material']] or '').strip().lstrip('0') or None
        if not code or code in seen:
            continue
        seen.add(code)
        name = ' '.join(str(r[col['material_description']] or code).split())
        price = r[col['price']] if isinstance(r[col['price']], (int, float)) else None
        status = 'Inactive' if str(r[col['status']] or '').strip().lower() == 'inactive' else 'Active'
        values.append(f"  ({lit(code)}, {lit(name)}, {lit(str(r[col['bun']] or '').strip() or None)}, {lit(price)}, {lit(status)})")
    out = ['-- CFO วัสดุจาก SAP (master_sto.xlsx แผ่น usage) · สร้างจาก scripts/import_cfo_material.py · รันใน Tx Data หลัง db/act/cfo.sql · รันซ้ำได้',
           f'-- {len(values)} รายการ · รันซ้ำแก้เฉพาะชื่อ หน่วย ราคา (EF และตัวแปลงที่จับคู่ไว้ไม่หาย)',
           'insert into public.mt_cfo_material (material, name, sap_unit, price, status) values',
           ',\n'.join(values),
           'on conflict (material) do update set name = excluded.name, sap_unit = excluded.sap_unit, price = excluded.price;', '']
    target = ROOT / 'inbox' / 'import_cfo_material.sql'
    target.write_text('\n'.join(out), encoding='utf-8', newline='\n')
    print(f'{target.relative_to(ROOT)} written ({len(values)} materials)')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'inbox' / 'master_sto.xlsx')

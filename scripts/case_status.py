"""Show the recorded progress of a modeling case without changing its files."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import re


HEADING = "## 进度与交接"
COLUMNS = ("范围", "阶段", "状态", "负责人", "证据或卡点", "下一步")
STATES = ("待开始", "进行中", "待复核", "通过", "需返工", "受阻", "不适用")
EMPTY = {"", "—"}


def read_progress(case_file):
    lines = case_file.read_text(encoding="utf-8-sig").splitlines()
    if HEADING not in lines:
        return None
    section = []
    for line in lines[lines.index(HEADING) + 1:]:
        if line.startswith(("# ", "## ")):
            break
        section.append(line)

    fields = {}
    rows = []
    for line in section:
        if line.startswith("- ") and "＝" in line:
            key, value = line[2:].split("＝", 1)
            fields[key.strip()] = value.strip()
        if line.startswith("|") and line.rstrip().endswith("|"):
            rows.append([cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]])
    if len(rows) < 2 or tuple(rows[0]) != COLUMNS:
        raise ValueError("请按 CASE 模板填写进度表的表头。")
    if len(rows[1]) != len(COLUMNS) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        raise ValueError("进度表缺少 Markdown 表格分隔行。")

    entries = {}
    for row in rows[2:]:
        if len(row) != len(COLUMNS):
            raise ValueError("进度表每行需要六列。单元格内的竖线请加反斜杠。")
        scope, stage, state, owner, evidence, next_step = row
        if scope in EMPTY or stage in EMPTY or state not in STATES:
            raise ValueError(f"检查进度表中的范围、阶段或状态：{' / '.join(row[:3])}")
        if (scope, stage) in entries:
            raise ValueError(f"进度表重复：{scope} / {stage}")
        if state in ("通过", "待复核", "需返工", "受阻", "不适用") and evidence in EMPTY:
            raise ValueError(f"请补上证据、卡点或不适用的理由：{scope} / {stage}")
        entries[scope, stage] = state, owner, evidence, next_step
    return fields, entries


def read_time(fields, name):
    value = fields.get(name, "")
    if value in EMPTY:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        parsed = None
    if parsed is None or parsed.utcoffset() is None:
        raise ValueError(f"{name}请填写带时区的时间，例如 2026-11-30T09:00:00+08:00。")
    return parsed


def display(fields, entries):
    deadline = read_time(fields, "官方截止")
    finalization = read_time(fields, "收尾开始")
    if deadline and finalization and finalization >= deadline:
        raise ValueError("收尾开始须早于官方截止。")

    now = datetime.now(timezone.utc)
    print(f"模式  {fields.get('工作模式') or '待确认'}")
    if deadline:
        minutes = int(abs((deadline - now).total_seconds()) // 60)
        hours, minutes = divmod(minutes, 60)
        label = "距官方截止" if now < deadline else "已过官方截止"
        print(f"{label}  {hours} 小时 {minutes} 分钟  ({deadline.isoformat(timespec='minutes')})")
    if finalization:
        label = "已进入收尾" if now >= finalization else "计划收尾"
        print(f"{label}  {finalization.isoformat(timespec='minutes')}")

    counts = Counter(value[0] for value in entries.values())
    print("进度  " + (" · ".join(f"{state} {counts[state]}" for state in STATES if counts[state]) or "暂无记录"))
    for (scope, stage), (state, owner, evidence, next_step) in entries.items():
        details = " · ".join(value for value in (owner, evidence, next_step) if value not in EMPTY)
        print(f"- {scope} / {stage} · {state}" + (f" · {details}" if details else ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path, help="CASE.md path or the directory containing it")
    args = parser.parse_args()
    case_file = args.case / "CASE.md" if args.case.is_dir() else args.case
    try:
        progress = read_progress(case_file)
        if progress is None:
            print("这份 CASE.md 未填写「进度与交接」。可按模板补入该节并沿用已有记录。")
            return
        display(*progress)
    except (OSError, ValueError) as error:
        parser.exit(2, f"无法读取进度：{error}\n")


if __name__ == "__main__":
    main()

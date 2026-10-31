#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数模交付包机检 —— 只查「人不会主动查、模型不会主动做」的四件事。

用法:
    python check.py <交付包目录> [--json]

规则:
    R1 假设表标「未检验」，摘要/结论却出现对应推断      -> FAIL
    R2 摘要超一页 / 正文超篇幅                          -> WARN / FAIL
    R3 图片文件缺失、正文图表引用断链、图注缺单位        -> FAIL / WARN
    R4 参考文献条目不可解析（疑似编造或空条）            -> FAIL / WARN

退出码: 0 全过 / 1 存在 FAIL / 2 仅存在 WARN / 3 输入无效
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

UNIT_HINTS = (
    '单位', '（mm', '(mm', '（cm', '(cm', '（m）', '(m)', '（km', '(km',
    'kg', '（s', '(s)', '（min', 'min)', '℃', '°c', '（%', '(%)', '％',
    '（元', '(元', '万元', '亿元', '（人', '人次', '（h', 'hour', '（d', '天）',
    'm/s', 'km/h', '㎡', 'm2', 'm³', 'm3', 'mw', 'kw', '（万', '（个', '（吨',
)
UNCHECKED_MARKS = ('未检验', '未验证', '未做检验', '待检验', '❌')
SKIP_NAME = {'例', '示例', '假设', '—', '-', '---', ''}
STOP_SECTIONS = ('参考文献', '附录')


# ---------- 基础工具 ----------
def load_md(root: Path) -> list[tuple[Path, str]]:
    out = []
    for p in sorted(root.rglob('*.md')):
        if p.name.lower() == 'readme.md':
            continue
        try:
            out.append((p, p.read_text(encoding='utf-8', errors='ignore')))
        except OSError:
            continue
    return out


def split_sections(text: str) -> dict[str, str]:
    """按 markdown 标题切段，键为标题文本（小写去空格）。"""
    secs: dict[str, list[str]] = {}
    cur = '__head__'
    secs[cur] = []
    for line in text.splitlines():
        m = re.match(r'^\s{0,3}(#{1,6})\s+(.*)$', line)
        if m:
            cur = m.group(2).strip().lower().replace(' ', '')
            secs.setdefault(cur, [])
        else:
            secs.setdefault(cur, []).append(line)
    return {k: '\n'.join(v) for k, v in secs.items()}


def cn_len(s: str) -> int:
    """中文按 1 字、英文按 0.5 字估算，返回等效汉字数。"""
    cn = len(re.findall(r'[\u4e00-\u9fff]', s))
    en = len(re.findall(r'[A-Za-z0-9]+', s))
    return cn + en // 2


def tables(text: str) -> list[list[str]]:
    """提取 markdown 表格的行（按 | 切分）。"""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('|') and s.endswith('|') and s.count('|') >= 3:
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
                continue
            rows.append(cells)
    return rows


# ---------- R1 未检验假设是否溜进结论 ----------

def parse_unchecked(text: str) -> list[str]:
    """只从含「检验」列表格的该列取标记，避免尺寸符号/普通叙述误判。"""
    out, col, header_seen = [], None, False
    for line in text.splitlines():
        s = line.strip()
        if not (s.startswith('|') and s.endswith('|')):
            col, header_seen = None, False
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
            continue
        if not header_seen:
            header_seen = True
            idx = [j for j, c in enumerate(cells) if ('检验' in c or '验证' in c)]
            col = idx[0] if idx else None
            continue
        name = cells[0].strip().strip('*` ')
        if len(name) < 3 or name in SKIP_NAME or name == '假设':
            continue
        if col is None or col >= len(cells):
            continue
        cell = cells[col]
        if any(w in cell for w in ('已检验', '已验证', '通过', '安全', '✅')):
            continue
        if any(mk in cell for mk in UNCHECKED_MARKS):
            out.append(name)
    return out



_STOP = {'生成', '规则', '方法', '模型', '数据', '位置', '所有', '同一'}


def terms_of(name: str) -> list[str]:
    s = re.sub(r'^(忽略|未考虑|不考虑|采用|使用|假设)', '', name)
    out = []
    for x in re.split(r'[与和及、]', s):
        x = x.strip()
        if len(x) >= 3:
            out += [x, x[-2:]]
        elif len(x) == 2:
            out.append(x)
    out = [x for x in out if x not in _STOP and len(x) >= 2]
    return out or [name]


def rule1(files, findings):
    """跨文件比对：未检验假设不得出现在摘要/结论里。"""
    targets = ('摘要', 'abstract')
    concl_keys = ('结论', '结果', '模型评价', '评价与推广', '讨论')
    limit_keys = ('局限', '模型评价', '评价与推广', '不足')

    names = []
    for path, text in files:
        for name in parse_unchecked(text):
            names.append((name, path.name))

    if not names:
        findings.append(('PASS', 'R1', '未发现「未检验」假设条目，无需核对'))
        return

    scope, limited = [], []
    for path, text in files:
        if any(x in path.name.lower() for x in ('审查', 'audit', '机检')):
            continue
        for k, v in split_sections(text).items():
            if any(x in k for x in targets) or any(c in k for c in concl_keys):
                scope.append((path.name, v))
            if any(x in k for x in limit_keys):
                limited.append((path.name, v))

    if not scope:
        findings.append(('WARN', 'R1', f'有 {len(names)} 条未检验假设，但未找到摘要/结论段落，无法核对'))
        return

    hits, missing_limit = 0, []
    for name, src in names:
        core = name
        terms = terms_of(name)
        leaked = False
        for fname, blob in scope:
            for sent in re.split(r'[。；！？\n]', blob):
                if not any(x in sent for x in terms):
                    continue
                if not re.search(r'效率|功率|kW|MW|%', sent, re.I):
                    continue
                if any(w in sent for w in ('未检验', '未验证', '局限', '不成立', '需检验', '不含', '未计', '未建模', '折减', '上限')):
                    continue
                hits += 1
                leaked = True
                findings.append((
                    'FAIL', 'R1',
                    f'假设「{name}」（{src}）标为未检验，但 {fname} 的摘要/结论在未经限定的句子里使用它 → {sent.strip()[:80]}'
                ))
                break
            if leaked:
                break
        if leaked:
            continue
        in_limit = any(any(x in blob for x in terms) for _, blob in limited)
        if not in_limit:
            missing_limit.append(name)

    if hits == 0:
        findings.append(('PASS', 'R1', f'{len(names)} 条未检验假设未进入摘要/结论'))
    if missing_limit:
        findings.append((
            'WARN', 'R1',
            f'未检验假设未在「局限」中写明：{ "、".join(missing_limit[:4]) }（应作为局限列出）'
        ))


# ---------- R2 篇幅 ----------
def rule2(files, findings):
    ab_warn, ab_fail, body_warn, body_fail = 1300, 1800, 26000, 34000
    ab_len = body_len = 0
    ab_src = body_src = ''
    for path, text in files:
        secs = split_sections(text)
        for k, v in secs.items():
            if '摘要' in k or k == 'abstract':
                n = cn_len(v)
                if n > ab_len:
                    ab_len, ab_src = n, path.name
        stripped = text
        for stop in STOP_SECTIONS:
            idx = stripped.find(stop)
            if idx > 0:
                stripped = stripped[:idx]
                break
        n = cn_len(stripped)
        if n > body_len:
            body_len, body_src = n, path.name
    if ab_len == 0:
        findings.append(('WARN', 'R2', '未找到「摘要」段落，无法核对一页限制'))
    elif ab_len > ab_fail:
        findings.append(('FAIL', 'R2', f'{ab_src} 摘要约 {ab_len} 字，明显超过一页，需压到 1000–1200 字'))
    elif ab_len > ab_warn:
        findings.append(('WARN', 'R2', f'{ab_src} 摘要约 {ab_len} 字，接近/略超一页'))
    else:
        findings.append(('PASS', 'R2', f'摘要约 {ab_len} 字，一页内（{ab_src or "-"}）'))
    if body_len > body_fail:
        findings.append(('FAIL', 'R2', f'{body_src} 正文约 {body_len} 字，远超 20 页，需删减'))
    elif body_len > body_warn:
        findings.append(('WARN', 'R2', f'{body_src} 正文约 {body_len} 字，可能超过 20 页'))


# ---------- R3 图表 ----------
def rule3(files, findings):
    defined, referenced, imgs_total, no_unit = set(), set(), 0, 0
    broken = []
    for path, text in files:
        base = path.parent
        for m in re.finditer(r'!\[[^\]]*\]\(([^)\s]+)', text):
            src = m.group(1)
            if src.startswith(('http://', 'https://')):
                continue
            imgs_total += 1
            cand = (base / src) if not src.startswith('/') else Path(src)
            if not cand.exists() and not (path.parent.parent / src).exists():
                broken.append(f'{path.name} → {src}')
        for line in text.splitlines():
            s = line.strip()
            m = re.match(r'^(?:\*\*)?图\s*([0-9]+(?:[-–][0-9]+)?)', s)
            if m and len(s) > 6:
                defined.add(m.group(1))
        for m in re.finditer(r'图\s*([0-9]+(?:[-–][0-9]+)?)', text):
            referenced.add(m.group(1))
    for b in broken[:6]:
        findings.append(('FAIL', 'R3', f'图片文件不存在：{b}'))
    if imgs_total and not broken:
        findings.append(('PASS', 'R3', f'图片文件齐全（{imgs_total} 张）'))
    if not imgs_total:
        findings.append(('WARN', 'R3', '未发现图片引用，数模论文通常应有结果图'))
    missing = sorted(referenced - defined)
    if missing:
        findings.append(('FAIL', 'R3', f'正文引用了但图中未定义的编号：图{", 图".join(missing[:6])}'))
    elif referenced:
        findings.append(('PASS', 'R3', f'图表编号引用闭合（{len(referenced)} 处引用 / {len(defined)} 处图注）'))


def rule3b_unit(files, findings):
    checked, missing = 0, []
    for path, text in files:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if not re.match(r'^\s*(?:\*\*)?图\s*[0-9]+', line.strip()):
                continue
            checked += 1
            ctx = line + ' ' + (lines[i + 1] if i + 1 < len(lines) else '')
            low = ctx.lower()
            if not any(h in low for h in UNIT_HINTS):
                missing.append(f'{path.name}: {line.strip()[:40]}')
    if missing:
        findings.append(('WARN', 'R3', f'{len(missing)} 处图注未见单位，例如：' + missing[0]))
    elif checked:
        findings.append(('PASS', 'R3', f'{checked} 处图注均含单位提示'))


# ---------- R4 参考文献 ----------
def rule4(files, findings):
    total = 0
    bad, weak = [], []
    for path, text in files:
        lines = text.splitlines()
        start = None
        for i, line in enumerate(lines):
            if re.match(r'^\s{0,3}#{1,6}\s*参考文献', line) or line.strip() == '参考文献':
                start = i
                break
        if start is None:
            continue
        for line in lines[start + 1:]:
            if re.match(r'^\s{0,3}#{1,6}\s', line) and '附录' in line:
                break
            m = re.match(r'^\s*\[(\d+)\]\s*(.+)$', line)
            if not m:
                continue
            total += 1
            body = m.group(2).strip()
            if len(body) < 20:
                bad.append(body[:30] or '(空)')
                continue
            if re.search(r'https?://|doi\.org|10\.\d{4,9}/', body, re.I):
                continue
            if re.search(r'(19|20)\d{2}', body) and re.search(
                r'学报|杂志|出版社|Press|Journal|Conference|Proc|Springer|Elsevier|Wiley|Science|arXiv|Addison|Cambridge|Oxford|CRC|Prentice', body
            ):
                continue
            weak.append(body[:50])
    if bad:
        findings.append(('FAIL', 'R4', f'{len(bad)} 条参考文献过短/为空，疑似占位：{bad[0]}'))
    if weak:
        findings.append(('WARN', 'R4', f'{len(weak)} 条参考文献无 DOI/URL 且格式可疑，需逐条核验：{weak[0]}'))
    if total and not bad and not weak:
        findings.append(('PASS', 'R4', f'{total} 条参考文献均可解析'))
    if not total:
        findings.append(('WARN', 'R4', '未找到「参考文献」章节或条目'))



# ---------- R5 题目要求清单：缺项是否显形 ----------
def rule5(files, findings):
    found, bad, soft = False, [], []
    for path, text in files:
        if any(x in path.name.lower() for x in ('审查', 'audit')):
            continue
        for k, v in split_sections(text).items():
            if '要求清单' not in k and '覆盖清单' not in k:
                continue
            found = True
            for line in v.splitlines():
                s = line.strip()
                if not (s.startswith('|') and s.endswith('|')):
                    continue
                cells = [c.strip() for c in s.strip('|').split('|')]
                if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
                    continue
                last = cells[-1].strip('*` ')
                KEY = ('未做', '未用', '自拟', '替代')
                if last in KEY:
                    bad.append(s[:70])
                elif any(last.startswith(k) for k in KEY):
                    soft.append(s[:70])
    if not found:
        findings.append(('WARN', 'R5', '未见「题目要求清单」，无法核对逐问 / 逐项覆盖（Phase 1 应产出）'))
    elif bad:
        findings.append(('FAIL', 'R5', f'{len(bad)} 项落在未做 / 未用 / 自拟且未写理由：{bad[0]}'))
    elif soft:
        findings.append(('WARN', 'R5',
                         f'{len(soft)} 项为未做 / 未用 / 自拟（已给理由，但缺项本身必须显形）：{soft[0]}'))
    else:
        findings.append(('PASS', 'R5', '题目要求清单齐备，无未说明的缺项'))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('target', nargs='?', default='.', help='交付包目录')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    root = Path(args.target).expanduser().resolve()
    if not root.exists():
        print(f'目录不存在: {root}')
        return 1

    files = load_md(root)
    if not files:
        print(f'未找到 markdown 文件: {root}')
        return 3

    findings: list[tuple[str, str, str]] = []
    rule1(files, findings)
    rule2(files, findings)
    rule3(files, findings)
    rule3b_unit(files, findings)
    rule4(files, findings)
    rule5(files, findings)

    order = {'FAIL': 0, 'WARN': 1, 'PASS': 2}
    findings.sort(key=lambda x: (order[x[0]], x[1]))
    n_fail = sum(1 for f in findings if f[0] == 'FAIL')
    n_warn = sum(1 for f in findings if f[0] == 'WARN')

    if args.json:
        print(json.dumps({
            'root': str(root), 'files': [str(p) for p, _ in files],
            'fail': n_fail, 'warn': n_warn,
            'findings': [{'level': a, 'rule': b, 'msg': c} for a, b, c in findings],
        }, ensure_ascii=False, indent=2))
    else:
        print(f'== 数模交付包机检：{root} ==')
        print(f'   共 {len(files)} 个 md 文件\n')
        for lv, rule, msg in findings:
            print(f'[{lv}] {rule}  {msg}')
        verdict = ('不得交付：存在 FAIL，须修复或经人工复核后书面豁免'
                   if n_fail else ('可交付，但需处理警告' if n_warn else '可交付'))
        print(f'\n{len(findings)} 项检查 → {n_fail} FAIL / {n_warn} WARN → {verdict}')

    if n_fail:
        return 1
    return 2 if n_warn else 0


if __name__ == '__main__':
    sys.exit(main())

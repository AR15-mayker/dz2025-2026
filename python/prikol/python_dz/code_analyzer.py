#!/usr/bin/env python3
"""Code base analyzer.

Scans a directory recursively for files with given extensions and
produces a JSON report and a console summary.
"""
from pathlib import Path
import argparse
import json
from typing import List, Dict, Any

DEFAULT_EXTS = ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.md']


def analyze_project(project_path: Path, exts: List[str] = None) -> Dict[str, Any]:
    exts = exts or DEFAULT_EXTS
    exts = [e.lower() for e in exts]

    files_data = []
    stats_by_ext = {}
    total_size = 0
    total_lines = 0

    for p in project_path.rglob('*'):
        if p.is_file():
            suf = p.suffix.lower()
            if suf in exts:
                try:
                    text = p.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    text = ''

                lines = text.splitlines()
                num_lines = len(lines)
                # approximate logical lines: non-empty and not starting with comment markers
                logical = sum(1 for ln in lines if ln.strip() and not ln.strip().startswith('#') and not ln.strip().startswith('//'))

                size_kb = p.stat().st_size / 1024

                files_data.append({
                    'path': str(p.resolve()),
                    'ext': suf,
                    'size_kb': round(size_kb, 2),
                    'lines': num_lines,
                    'logical_lines_approx': logical,
                })

                total_size += p.stat().st_size
                total_lines += num_lines

                entry = stats_by_ext.setdefault(suf, {'files': 0, 'lines': 0, 'size_bytes': 0})
                entry['files'] += 1
                entry['lines'] += num_lines
                entry['size_bytes'] += p.stat().st_size

    # compute aggregates
    for suf, entry in stats_by_ext.items():
        entry['avg_lines_per_file'] = round(entry['lines'] / entry['files'], 2) if entry['files'] else 0
        entry['size_mb'] = round(entry['size_bytes'] / (1024 * 1024), 3)

    biggest_file = None
    if files_data:
        biggest = max(files_data, key=lambda f: f['lines'])
        biggest_file = {'path': biggest['path'], 'lines': biggest['lines']}

    report = {
        'project': str(project_path.resolve()),
        'summary': {
            'total_files': sum(e['files'] for e in stats_by_ext.values()),
            'total_size_mb': round(total_size / (1024 * 1024), 3),
            'total_lines': total_lines,
        },
        'by_extension': stats_by_ext,
        'biggest_file': biggest_file,
        'files': files_data,
    }

    return report


def print_summary(report: Dict[str, Any]):
    proj = report['project']
    s = report['summary']
    print(f"[Анализ кодовой базы проекта: {proj}]")
    print("=" * 60)
    print()
    print("Общая статистика:")
    print(f"• Всего файлов с кодом: {s['total_files']}")
    print(f"• Общий объем кода: {s['total_size_mb']} MB")
    print(f"• Общее количество строк: {s['total_lines']}")
    print()
    print("Детали по типам файлов:")
    for suf, entry in report['by_extension'].items():
        name = suf or '[no suffix]'
        print(f"[{name}] ({suf})")
        print(f"  Файлов: {entry['files']}, Строк: {entry['lines']}, Средний размер: {entry['avg_lines_per_file']} строк/файл")
        # find biggest of this extension
        # cheap search
        biggest = None
        for f in report['files']:
            if f['ext'] == suf:
                if biggest is None or f['lines'] > biggest['lines']:
                    biggest = f
        if biggest:
            print(f"  Самый большой файл: {biggest['path']} ({biggest['lines']} строк)")
        print()


def main():
    parser = argparse.ArgumentParser(description='Analyze code base statistics')
    parser.add_argument('path', nargs='?', default='.', help='Path to project root')
    parser.add_argument('--ext', '-e', nargs='*', help='List of file extensions to include')
    parser.add_argument('--out', '-o', default='code_analysis_report.json', help='Output JSON file')

    args = parser.parse_args()
    project = Path(args.path)
    exts = args.ext

    report = analyze_project(project, exts)
    print_summary(report)

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Отчёт сохранён в: {args.out}")


if __name__ == '__main__':
    main()

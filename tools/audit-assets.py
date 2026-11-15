#!/usr/bin/env python3
"""資產體積盤點腳本。

用法：
    python3 tools/audit-assets.py [門檻KB]

依目錄統計大小，並列出超過門檻（預設 200 KB）的檔案，做為優化候選參考。
注意：moon/moon-height.bin 為自訂二進位格式，不可重編。
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIES = ["models", "moon", "sfx", "ui", "vfx", "locales"]
THRESHOLD_KB = float(sys.argv[1]) if len(sys.argv) > 1 else 200.0


def human(size):
    if size >= 1024 * 1024:
        return f"{size / 1024 / 1024:.2f} MB"
    return f"{size / 1024:.1f} KB"


def main():
    grand_total = 0
    large = []

    for cat in CATEGORIES:
        base = os.path.join(ROOT, cat)
        if not os.path.isdir(base):
            continue
        total = 0
        entries = []
        for dirpath, _, filenames in os.walk(base):
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                size = os.path.getsize(path)
                total += size
                entries.append((size, os.path.relpath(path, ROOT)))
                if size >= THRESHOLD_KB * 1024:
                    large.append((size, os.path.relpath(path, ROOT)))
        grand_total += total
        entries.sort(reverse=True)
        print(f"\n[{cat}] 總計 {human(total)}（{len(entries)} 檔）")
        for size, rel in entries[:5]:
            print(f"  {human(size):>10}  {rel}")

    html = os.path.join(ROOT, "index.html")
    if os.path.isfile(html):
        size = os.path.getsize(html)
        grand_total += size
        print(f"\n[index.html] {human(size)}")

    print(f"\n全體（不含 .git）：{human(grand_total)}")

    large.sort(reverse=True)
    print(f"\n超過 {THRESHOLD_KB:.0f} KB 的檔案：")
    if not large:
        print("  （無）")
    for size, rel in large:
        print(f"  {human(size):>10}  {rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

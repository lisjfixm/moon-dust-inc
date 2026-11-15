#!/usr/bin/env python3
"""比對 locales/*.json 的鍵集合是否一致。

用法：
    python3 tools/check-locales.py

所有語言檔應與參考檔（排序後第一個）擁有相同鍵集合；
不一致時印出缺鍵 / 多餘鍵，並以離開碼 1 結束。
英文為程式內建 fallback，不在 locales/ 目錄中。
"""

import json
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALE_DIR = os.path.join(ROOT, "locales")


def flatten(obj, prefix=""):
    """將巢狀物件攤平為 dotted key 集合。"""
    keys = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            name = f"{prefix}.{k}" if prefix else k
            keys |= flatten(v, name)
    else:
        keys.add(prefix)
    return keys


def main():
    files = sorted(glob.glob(os.path.join(LOCALE_DIR, "*.json")))
    if not files:
        print("找不到 locales/*.json", file=sys.stderr)
        return 1

    reference = None
    reference_name = None
    mismatch = False

    for path in files:
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        keys = flatten(data)
        if reference is None:
            reference = keys
            reference_name = name
            print(f"參考語言：{name}（{len(keys)} 鍵）")
            continue

        missing = reference - keys
        extra = keys - reference
        if missing or extra:
            mismatch = True
            print(f"✗ {name}")
            if missing:
                print(f"    缺鍵：{sorted(missing)}")
            if extra:
                print(f"    多餘鍵：{sorted(extra)}")
        else:
            print(f"✓ {name}（{len(keys)} 鍵）")

    if mismatch:
        print("\n語言檔鍵值不一致，請同步缺漏的文案。", file=sys.stderr)
        return 1

    print(f"\n全部 {len(files)} 個語言檔鍵值對齊（參考 {reference_name}）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

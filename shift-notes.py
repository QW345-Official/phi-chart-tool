import json
import os
import sys

# ─────────────────────────── 配置 ───────────────────────────
INPUT_FILE = r"C:\Users\helloworld\Desktop\rrat.json"
OUTPUT_FILE = r"C:\Users\helloworld\Desktop\rrat但是键放歪了.json"


def shift_notes(chart):
    """
    对每根判定线的 notesAbove / notesBelow，
    按 time 分组，整体平移到下一个时间点。
    最后一组用最后两组的间隔继续平移。
    """
    for line in chart.get("judgeLineList", []):
        for key in ("notesAbove", "notesBelow"):
            notes = line.get(key, [])
            if not notes:
                continue

            # 按 time 分组（保留原顺序无关，time 相同的归一组）
            times = sorted(set(n["time"] for n in notes))
            if len(times) == 1:
                # 只有一个时间点，无法平移，保持原样
                continue

            # 建立映射：旧时间 -> 新时间
            mapping = {}
            for i, t in enumerate(times):
                if i + 1 < len(times):
                    mapping[t] = times[i + 1]
                else:
                    # 最后一组：用最后一组的间隔
                    gap = times[-1] - times[-2]
                    mapping[t] = times[-1] + gap

            # 应用映射
            for n in notes:
                n["time"] = mapping[n["time"]]

    return chart


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[错误] 找不到 {INPUT_FILE}")
        return

    with open(INPUT_FILE, encoding="utf-8") as f:
        chart = json.load(f)

    print(f"[读取] {INPUT_FILE}")
    chart = shift_notes(chart)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chart, f, ensure_ascii=False, separators=(",", ":"))

    print(f"[写出] {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

import xml.etree.ElementTree as ET
from pathlib import Path
import json

# 解析対象のFM-7系プロジェクト
TARGETS = ["fm7", "fm77", "fm77l4", "fm77av", "fm77av40", "fm77av40ex"]
PROJ_DIR = Path("source/vc++2017")
REPO_ROOT = Path(".").resolve()

def parse_vcxproj(vcxproj_path: Path):
    tree = ET.parse(vcxproj_path)
    root = tree.getroot()
    # XML名前空間を取得
    ns = {"ms": root.tag.split("}")[0].strip("{")} if "}" in root.tag else {}

    sources = []
    headers = []

    for item in root.findall(".//ms:ClCompile", ns):
        inc = item.attrib.get("Include")
        if inc:
            p = (vcxproj_path.parent / inc.replace("\\", "/")).resolve()
            rel = p.relative_to(REPO_ROOT).as_posix()
            sources.append(rel)

    for item in root.findall(".//ms:ClInclude", ns):
        inc = item.attrib.get("Include")
        if inc:
            p = (vcxproj_path.parent / inc.replace("\\", "/")).resolve()
            rel = p.relative_to(REPO_ROOT).as_posix()
            headers.append(rel)

    return sorted(set(sources)), sorted(set(headers))

def main():
    per_target = {}
    all_sources = set()
    all_headers = set()

    for target in TARGETS:
        vcxproj = PROJ_DIR / f"{target}.vcxproj"
        if not vcxproj.exists():
            print(f"[WARN] Not found: {vcxproj}")
            continue
        srcs, hdrs = parse_vcxproj(vcxproj)
        per_target[target] = {"sources": srcs, "headers": hdrs}
        all_sources.update(srcs)
        all_headers.update(hdrs)
        print(f"[{target}] sources: {len(srcs)}, headers: {len(hdrs)}")

    # 結果をJSONファイルに保存（後続のCMake生成やスリム化に使用）
    out_data = {
        "targets": per_target,
        "all_sources": sorted(all_sources),
        "all_headers": sorted(all_headers),
    }
    out_path = Path("tools/fm7_files.json")
    out_path.write_text(json.dumps(out_data, indent=2), encoding="utf-8")

    # 機種別に「共通のソース」と「機種固有のソース」を分類して表示
    common_sources = set.intersection(*(set(v["sources"]) for v in per_target.values()))
    print("\n=== Summary ===")
    print(f"Total unique sources : {len(all_sources)}")
    print(f"Total unique headers : {len(all_headers)}")
    print(f"Common sources (all 6 models): {len(common_sources)}")
    print(f"Saved detailed list to: {out_path}")

    # 使われているサブディレクトリ一覧を表示（スリム化時のホワイトリスト確認用）
    used_dirs = sorted({Path(p).parent.as_posix() for p in (all_sources | all_headers)})
    print("\n=== Used Directories ===")
    for d in used_dirs:
        print(f"  {d}")

if __name__ == "__main__":
    main()

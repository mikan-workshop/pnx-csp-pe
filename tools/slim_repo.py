import json
import os
import re
import shutil
import argparse
from pathlib import Path

REPO_ROOT = Path(".").resolve()
JSON_PATH = REPO_ROOT / "tools/fm7_files.json"

# FM-7系のプロジェクトファイル名
KEEP_TARGETS = {"fm7", "fm77", "fm77l4", "fm77av", "fm77av40", "fm77av40ex"}

# インクルード検索パス（CSP標準の検索パス）
INCLUDE_DIRS = [
    REPO_ROOT / "source/src",
    REPO_ROOT / "source/src/vm",
    REPO_ROOT / "source/src/vm/fm7",
    REPO_ROOT / "source/src/vm/fmgen",
    REPO_ROOT / "source/src/win32",
    REPO_ROOT / "source/src/res",
]

INCLUDE_PATTERN = re.compile(r'^\s*#\s*include\s*"([^"]+)"', re.MULTILINE)


def resolve_include(current_file: Path, inc_str: str) -> Path | None:
    inc_rel = inc_str.replace("\\", "/")
    # 1. 現在のファイルからの相対パスで探す
    cand = (current_file.parent / inc_rel).resolve()
    if cand.is_file():
        return cand
    # 2. 共通インクルードパスから探す
    for base in INCLUDE_DIRS:
        cand = (base / inc_rel).resolve()
        if cand.is_file():
            return cand
    return None


def collect_dependencies(initial_files: set[Path]) -> set[Path]:
    keep = set(initial_files)
    queue = list(initial_files)

    while queue:
        curr = queue.pop(0)
        if not curr.is_file():
            continue
        try:
            text = curr.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue

        for match in INCLUDE_PATTERN.finditer(text):
            inc_target = match.group(1)
            resolved = resolve_include(curr, inc_target)
            if resolved and resolved not in keep:
                # リポジトリ内のファイルであれば保護リストに追加
                try:
                    resolved.relative_to(REPO_ROOT)
                    keep.add(resolved)
                    queue.append(resolved)
                except ValueError:
                    pass
    return keep


def main():
    parser = argparse.ArgumentParser(description="Slim down pnx-csp-pe to FM-7 series only.")
    parser.add_argument("--execute", action="store_true", help="Actually delete unused files.")
    args = parser.parse_args()

    if not JSON_PATH.exists():
        print(f"[ERROR] {JSON_PATH} not found. Run extract_fm7_files.py first.")
        return

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    initial_files = set()
    for p_str in data["all_sources"] + data["all_headers"]:
        initial_files.add((REPO_ROOT / p_str).resolve())

    # 1. #include 依存関係を再帰的に追跡して保護対象を確定
    keep_files = collect_dependencies(initial_files)
    print(f"Initial files from vcxproj : {len(initial_files)}")
    print(f"Total protected files      : {len(keep_files)} (including nested #includes)")

    # 2. source/src/ 内の削除対象ファイルをリストアップ
    src_root = REPO_ROOT / "source/src"
    files_to_delete = []
    for p in src_root.rglob("*"):
        if p.is_file() and p.resolve() not in keep_files:
            # zlib ライブラリフォルダは保護する
            if (src_root / "zlib-1.2.11") in p.parents:
                continue
            # FM-7用の .rc や .ico、共通の afxres.h / vista.manifest は残す
            if (src_root / "res") in p.parents and (
                p.parent.name == "indicator"
                or p.name.lower() in {"afxres.h", "vista.manifest"}
                or any(t in p.stem.lower() for t in ["fm7", "fm8"])
            ):
                continue
            files_to_delete.append(p)

    # 3. source/vc++2017/ 内の他機種プロジェクトファイルをリストアップ
    vc_dir = REPO_ROOT / "source/vc++2017"
    if vc_dir.exists():
        for p in vc_dir.iterdir():
            if p.is_file():
                # FM-7系のプロジェクトファイルと build_fm7.bat 以外は削除対象
                if p.suffix.lower() in {".vcxproj", ".filters", ".user"}:
                    base_name = p.name.split(".")[0].lower()
                    if base_name not in KEEP_TARGETS:
                        files_to_delete.append(p)
                elif p.name.lower() == "build.bat":
                    files_to_delete.append(p)

    # 4. vendor_source/ フォルダの削除対象確認
    vendor_dir = REPO_ROOT / "vendor_source"

    print(f"\nFiles to delete in source/ : {len(files_to_delete)}")
    if vendor_dir.exists():
        print(f"Directory to delete        : {vendor_dir.relative_to(REPO_ROOT)}")

    if not args.execute:
        print("\n[DRY-RUN] No files were deleted.")
        print("Sample files to be deleted (first 15):")
        for f in sorted(files_to_delete)[:15]:
            print(f"  - {f.relative_to(REPO_ROOT).as_posix()}")
        print("\nRun with '--execute' to actually remove these files.")
        return

    # 削除の実行
    for f in files_to_delete:
        f.unlink(missing_ok=True)

    if vendor_dir.exists():
        shutil.rmtree(vendor_dir)

    # 空になったサブディレクトリをクリーンアップ
    for dirpath, dirnames, filenames in os.walk(src_root, topdown=False):
        d = Path(dirpath)
        if d != src_root and not any(d.iterdir()):
            d.rmdir()

    print("\n[DONE] Slimming completed! Run 'git status' to review changes.")


if __name__ == "__main__":
    main()

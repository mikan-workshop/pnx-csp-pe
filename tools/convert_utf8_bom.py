import os
from pathlib import Path

# 変換対象とするソース・テキスト系の拡張子
TARGET_EXTS = {
    ".c", ".cpp", ".cc", ".cxx",
    ".h", ".hpp", ".hh", ".hxx",
    ".def", ".inl", ".inc",
    ".txt", ".md"
}

# 除外するディレクトリ
EXCLUDE_DIRS = {".git", ".vs", "Debug", "Release", "x64", "x86", "res"}
EXCLUDE_FILES = {"resource.h"}

def convert_file(filepath: Path) -> str:
    raw = filepath.read_bytes()

    # すでに UTF-8 BOM (EF BB BF) が付いている場合はスキップ
    if raw.startswith(b"\xef\xbb\xbf"):
        return "skip_bom"

    # バイナリ判定（NULLバイトが含まれていたらスキップ）
    if b"\x00" in raw:
        return "skip_bin"

    # まず UTF-8 (BOMなし) として読めるか試す（ASCIIのみのファイルもここに該当）
    try:
        text = raw.decode("utf-8")
        # ASCIIのみ、または既にUTF-8だったファイルにもBOM付きUTF-8として統一保存
        filepath.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
        return "utf8_to_bom"
    except UnicodeDecodeError:
        pass

    # CP932 (Windows Shift-JIS) としてデコードして UTF-8 (BOM付き) に変換
    try:
        text = raw.decode("cp932")
        filepath.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
        return "cp932_to_bom"
    except UnicodeDecodeError as e:
        print(f"[WARN] Decode failed: {filepath} ({e})")
        return "error"

def main():
    root = Path(".")
    stats = {"cp932_to_bom": 0, "utf8_to_bom": 0, "skip_bom": 0, "skip_bin": 0, "error": 0}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.lower() in EXCLUDE_FILES:
                continue
            p = Path(dirpath) / fname
            if p.suffix.lower() in TARGET_EXTS:
                res = convert_file(p)
                stats[res] += 1

    print("=== Conversion Complete ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()

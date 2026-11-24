"""Preflight the APMCM 2026 AI disclosure PDF in a submission directory."""

import argparse
from pathlib import Path


PDF_NAME = "AI工具使用详情.pdf"


def check_disclosure(directory):
    entries = {path.name: path for path in directory.iterdir()}
    expected = entries.get(PDF_NAME)
    if expected is None or not expected.is_file():
        nearby = sorted(name for name in entries if "AI工具使用详情" in name)
        detail = f" 找到 {', '.join(nearby)}。" if nearby else ""
        raise ValueError(f"请把披露 PDF 的完整文件名设为 {PDF_NAME}。{detail}")
    with expected.open("rb") as document:
        if not document.read(8).startswith(b"%PDF-"):
            raise ValueError(f"{PDF_NAME} 需要从编辑器导出为 PDF。")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="folder containing the final submission files")
    args = parser.parse_args()
    try:
        check_disclosure(args.directory)
    except (ValueError, OSError) as error:
        parser.exit(2, f"{error}\n")
    print(f"{PDF_NAME} 文件名和 PDF 文件头通过。请打开文件核对正文与披露内容。")


if __name__ == "__main__":
    main()

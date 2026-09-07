"""
Package V3.1 Complete Research Dossier & Artifacts ZIP Archive
==============================================================
Packs all research scripts, dossiers, markdown reports, cloud backtest summaries,
and trade logs into an organized, downloadable ZIP archive.
"""

import os
import sys
import zipfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_ZIP = os.path.join(ROOT_DIR, "KCEX_V3_1_QUANT_RESEARCH_DOSSIER_AND_ARTIFACTS.zip")

def package_artifacts():
    print("=" * 80)
    print("[*] PACKAGING COMPREHENSIVE V3.1 QUANT RESEARCH DOSSIER & ARTIFACTS ZIP")
    print(f"[*] Target Destination: {OUTPUT_ZIP}")
    print("=" * 80)

    # Directories to include
    include_dirs = [
        ("AI_ANALYSIS/Analysis - V3", "AI_ANALYSIS/Analysis - V3"),
        ("BACKTESTER/cloud_reports", "BACKTESTER/cloud_reports"),
        ("research_v3", "research_v3")
    ]

    # Individual files to include
    include_files = [
        "settings.py",
        ".env.example",
        "requirements.txt"
    ]

    total_files = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add directories
        for rel_dir, arc_base in include_dirs:
            abs_dir = os.path.join(ROOT_DIR, rel_dir)
            if not os.path.exists(abs_dir):
                continue
            for root, _, files in os.walk(abs_dir):
                for f in files:
                    if f.endswith((".pyc", ".git", ".DS_Store")):
                        continue
                    full_path = os.path.join(root, f)
                    arc_name = os.path.relpath(full_path, ROOT_DIR)
                    zf.write(full_path, arc_name)
                    total_files += 1

        # Add root files
        for f in include_files:
            full_path = os.path.join(ROOT_DIR, f)
            if os.path.exists(full_path):
                zf.write(full_path, f)
                total_files += 1

    file_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\n[OK] Successfully packaged {total_files} files into ZIP archive.")
    print(f"[*] Archive Size: {file_size_mb:.2f} MB")
    print(f"[*] Absolute Path: {OUTPUT_ZIP}")

    # Also copy to parent workspace root for easy user access
    parent_zip = os.path.join(os.path.dirname(ROOT_DIR), "KCEX_V3_1_QUANT_RESEARCH_DOSSIER_AND_ARTIFACTS.zip")
    try:
        import shutil
        shutil.copy2(OUTPUT_ZIP, parent_zip)
        print(f"[*] Copied duplicate to parent workspace root: {parent_zip}")
    except Exception as e:
        print(f"[!] Could not copy to parent: {e}")

if __name__ == "__main__":
    package_artifacts()

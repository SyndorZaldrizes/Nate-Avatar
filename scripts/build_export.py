import argparse
import datetime
import json
import re
import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


REPO_NAME = "SyndorZaldrizes/Nate-Avatar"
ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "exports" / "export-manifest.json"
DIST_DIR = ROOT / "dist"
PACK_JSON = DIST_DIR / "altius-pack.json"
PACK_ZIP = DIST_DIR / "altius-pack.zip"


def load_manifest():
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Missing manifest file at {MANIFEST_PATH}")
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    paths = data.get("paths", [])
    if not isinstance(paths, list):
        raise ValueError("export-manifest.json must contain a 'paths' array")
    return paths


def resolve_version():
    package_json = ROOT / "package.json"
    if package_json.exists():
        with package_json.open("r", encoding="utf-8") as f:
            pkg = json.load(f)
        version = pkg.get("version")
        if version:
            return str(version)

    changelog = ROOT / "CHANGELOG.md"
    version_pattern = re.compile(r"^##\s+v?([0-9A-Za-z\.-]+)")
    if changelog.exists():
        with changelog.open("r", encoding="utf-8") as f:
            for line in f:
                match = version_pattern.match(line.strip())
                if match:
                    return match.group(1)
    return "0.0.0"


def collect_files(base_path: Path, scope: str):
    files = {}
    for file_path in sorted(base_path.rglob("*")):
        if file_path.is_file():
            rel = Path(scope) / file_path.relative_to(base_path)
            rel_posix = rel.as_posix()
            files[rel_posix] = file_path.read_text(encoding="utf-8")
    return files


def include_entry(entry):
    include_flag = entry.get("include", True)
    optional = entry.get("optional", False)
    if include_flag:
        return True
    return False if optional else False


def build_bundle():
    manifest_entries = load_manifest()

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "version": resolve_version(),
        "generated_at": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
        "source_repo": REPO_NAME,
    }

    archive_sources = []

    for entry in manifest_entries:
        path_value = entry.get("path")
        entry_type = entry.get("type")
        if not path_value or not entry_type:
            raise ValueError("Each manifest entry requires 'path' and 'type' keys")
        if not include_entry(entry):
            continue

        target_path = ROOT / path_value
        if entry_type == "directory":
            if not target_path.is_dir():
                raise FileNotFoundError(f"Expected directory: {path_value}")
            files = collect_files(target_path, path_value)
            key_name = path_value.lower()
            data[key_name] = files
            archive_sources.extend(sorted(files.keys()))
        elif entry_type == "file":
            if not target_path.is_file():
                raise FileNotFoundError(f"Expected file: {path_value}")
            if path_value == "identity-schema.json":
                with target_path.open("r", encoding="utf-8") as f:
                    data["identity_schema"] = json.load(f)
            else:
                data[path_value] = target_path.read_text(encoding="utf-8")
            archive_sources.append(path_value)
        else:
            raise ValueError(f"Unknown entry type: {entry_type}")

    required_sections = ["identity_schema", "persona", "modules", "safeguards", "prompts"]
    for section in required_sections:
        if section not in data:
            raise ValueError(f"Missing required section in bundle: {section}")

    with PACK_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with ZipFile(PACK_ZIP, "w", ZIP_DEFLATED) as zf:
        for rel_path in sorted(archive_sources):
            abs_path = ROOT / rel_path
            zf.write(abs_path, arcname=rel_path)

    print(f"Export created at {PACK_JSON} and {PACK_ZIP}")


def verify_bundle():
    manifest_entries = load_manifest()
    missing_paths = []
    for entry in manifest_entries:
        if not include_entry(entry):
            continue
        path_value = entry.get("path")
        entry_type = entry.get("type")
        target = ROOT / path_value
        if entry_type == "directory" and not target.is_dir():
            missing_paths.append(path_value)
        if entry_type == "file" and not target.is_file():
            missing_paths.append(path_value)

    if missing_paths:
        raise FileNotFoundError(f"Missing required export inputs: {', '.join(missing_paths)}")

    if not PACK_JSON.exists():
        raise FileNotFoundError(f"Bundle not found at {PACK_JSON}. Run the build first.")

    with PACK_JSON.open("r", encoding="utf-8") as f:
        bundle = json.load(f)

    required_keys = ["version", "generated_at", "source_repo", "identity_schema", "persona", "modules", "safeguards", "prompts"]
    missing_keys = [k for k in required_keys if k not in bundle]
    if missing_keys:
        raise KeyError(f"altius-pack.json is missing keys: {', '.join(missing_keys)}")

    print("Verification passed: all required inputs and bundle keys are present.")


def clean_dist():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print(f"Removed {DIST_DIR}")
    else:
        print("Nothing to clean.")


def main():
    parser = argparse.ArgumentParser(description="Build and verify deterministic Altius exports.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build", help="Build the export bundle")
    subparsers.add_parser("verify", help="Verify the export bundle and inputs")
    subparsers.add_parser("clean", help="Remove generated artifacts")

    args = parser.parse_args()

    if args.command == "build":
        build_bundle()
    elif args.command == "verify":
        verify_bundle()
    elif args.command == "clean":
        clean_dist()


if __name__ == "__main__":
    main()

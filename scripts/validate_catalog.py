#!/usr/bin/env python3

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "catalog.json"
REQUIRED_FIELDS = {
    "id",
    "name",
    "description",
    "category",
    "scenarios",
    "technologies",
    "maturity",
    "repositoryUrl",
    "maintainers",
    "lastReviewed",
}
ALLOWED_FIELDS = REQUIRED_FIELDS | {
    "industries",
    "tags",
    "documentationUrl",
}
CATEGORIES = {
    "accelerator",
    "reference-architecture",
    "sample",
    "tool",
    "best-practice",
}
MATURITY_LEVELS = {"experimental", "preview", "production", "archived"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_string_list(asset_id: str, field: str, value: object) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        return [f"{asset_id}: '{field}' must be a non-empty list of strings"]
    if len(value) != len(set(value)):
        return [f"{asset_id}: '{field}' must not contain duplicates"]
    return []


def validate_url(asset_id: str, field: str, value: object) -> list[str]:
    if not isinstance(value, str):
        return [f"{asset_id}: '{field}' must be a URL string"]
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        return [f"{asset_id}: '{field}' must be an HTTPS URL"]
    return []


def validate_asset(asset: object, index: int) -> list[str]:
    if not isinstance(asset, dict):
        return [f"assets[{index}] must be an object"]

    asset_id = str(asset.get("id", f"assets[{index}]"))
    errors: list[str] = []
    missing = REQUIRED_FIELDS - asset.keys()
    unexpected = asset.keys() - ALLOWED_FIELDS
    if missing:
        errors.append(f"{asset_id}: missing fields: {', '.join(sorted(missing))}")
    if unexpected:
        errors.append(
            f"{asset_id}: unexpected fields: {', '.join(sorted(unexpected))}"
        )

    if not ID_PATTERN.fullmatch(str(asset.get("id", ""))):
        errors.append(f"{asset_id}: 'id' must be lowercase kebab-case")
    if asset.get("category") not in CATEGORIES:
        errors.append(f"{asset_id}: unsupported category")
    if asset.get("maturity") not in MATURITY_LEVELS:
        errors.append(f"{asset_id}: unsupported maturity")

    for field in ("scenarios", "technologies", "maintainers"):
        errors.extend(validate_string_list(asset_id, field, asset.get(field)))
    for field in ("industries", "tags"):
        if field in asset:
            errors.extend(validate_string_list(asset_id, field, asset[field]))

    errors.extend(validate_url(asset_id, "repositoryUrl", asset.get("repositoryUrl")))
    repository_url = asset.get("repositoryUrl")
    if isinstance(repository_url, str):
        parsed = urlparse(repository_url)
        if parsed.netloc.lower() != "github.com" or len(parsed.path.strip("/").split("/")) != 2:
            errors.append(f"{asset_id}: 'repositoryUrl' must identify a GitHub repository")
    if "documentationUrl" in asset:
        errors.extend(
            validate_url(asset_id, "documentationUrl", asset["documentationUrl"])
        )

    try:
        date.fromisoformat(str(asset.get("lastReviewed", "")))
    except ValueError:
        errors.append(f"{asset_id}: 'lastReviewed' must use YYYY-MM-DD")

    return errors


def main() -> int:
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to read catalog: {error}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if not isinstance(catalog, dict):
        errors.append("Catalog root must be an object")
        assets: object = []
    else:
        if catalog.get("version") != 1:
            errors.append("Catalog 'version' must be 1")
        assets = catalog.get("assets")

    if not isinstance(assets, list):
        errors.append("Catalog 'assets' must be an array")
        assets = []

    seen_ids: set[str] = set()
    for index, asset in enumerate(assets):
        errors.extend(validate_asset(asset, index))
        if isinstance(asset, dict) and isinstance(asset.get("id"), str):
            asset_id = asset["id"]
            if asset_id in seen_ids:
                errors.append(f"{asset_id}: duplicate id")
            seen_ids.add(asset_id)

    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Catalog is valid ({len(assets)} assets).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


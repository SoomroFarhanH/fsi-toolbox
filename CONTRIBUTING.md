# Contributing to the FSI Toolbox

Thank you for helping make FSI assets easier to discover and reuse.

## Add an asset

1. Fork this repository and create a branch.
2. Add one object to the `assets` array in `catalog/catalog.json`.
3. Use a stable, lowercase, hyphen-separated `id`.
4. Confirm the source repository is accessible to the catalog's intended
   audience and has a license, documentation, and named maintainers.
5. Run `python scripts/validate_catalog.py`.
6. Open a pull request using the repository template.

You can also open an asset proposal issue if you do not want to prepare a pull
request.

## Catalog entry fields

Required fields:

- `id`: unique lowercase identifier.
- `name`: human-readable asset name.
- `description`: concise statement of purpose and value.
- `category`: one of `accelerator`, `reference-architecture`, `sample`, `tool`,
  or `best-practice`.
- `scenarios`: one or more customer or business scenarios.
- `technologies`: primary platforms, services, or languages.
- `maturity`: `experimental`, `preview`, `production`, or `archived`.
- `repositoryUrl`: HTTPS URL of the source repository.
- `maintainers`: one or more GitHub handles without the `@` prefix.
- `lastReviewed`: date in `YYYY-MM-DD` format.

Optional fields:

- `industries`: FSI segments such as banking, insurance, or capital markets.
- `tags`: additional discovery terms.
- `documentationUrl`: primary documentation URL.

## Acceptance criteria

Maintainers review submissions for:

- clear relevance to an FSI customer or business scenario;
- useful documentation and a straightforward getting-started experience;
- an appropriate open-source license and no embedded secrets or customer data;
- explicit security, privacy, compliance, and responsible AI considerations
  where applicable;
- ownership and maintenance expectations; and
- no unnecessary duplication of an existing catalog entry.

Catalog inclusion is not a Microsoft product endorsement or a support
commitment. Reviewers may request changes or decline assets that do not meet
these criteria.

## Pull requests

Keep changes focused. Update an existing entry when ownership, maturity,
location, or review status changes. By contributing, you agree that your
contribution is licensed under this repository's MIT License.

## Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).


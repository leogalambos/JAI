# Deployment notes

## Operating model for an enterprise deployment

Once installed, **users interact with Claude/Codex**, not a library of manually invoked scripts. Administrators own configuration, permissions, credentials and release qualification. The provider orchestrates specialist agents and authorised internal tool calls; the organisation supplies accountable decision owners and a trusted L0 approval channel. The Codex implementation intentionally requires human-run protected L0 actions outside the agent's tool path. A pilot should verify these distinctions with real provider sessions and representative denial/approval cases, in addition to structural package tests.

## Recommended adoption path

For most organisations, a sensible adoption path is:

1. **single-user evaluation** using the demo estate;
2. **team pilot** focused on one or two concrete deliverables;
3. **controlled rollout** with local policy review and model-routing governance;
4. **integration into enterprise working methods** and repositories.

## Workstation vs shared build image

The package is installed locally, but enterprise teams often prefer to standardise optional dependencies such as LibreOffice, Pandoc and validation libraries in a shared developer workstation image or managed VDI.

Qualify that image inside the actual provider sandbox as well as in a system terminal. Installed executables can still fail when their resources, fonts, TeX formats, resolver state or temporary directories are inaccessible. Use [sandbox and environment prerequisites](sandbox-prerequisites.md) to select task-specific dependencies and access. Administrators own the effective policy; local rendering does not justify broad filesystem writes or unrestricted network access.

## What to lock down before wider rollout

- provider permissions and operating mode;
- allowed network behaviour;
- local or central model overrides;
- approval authority roles;
- retention handling for `.findings/` and `.fabric/` records;
- document classification and publication controls.

## When to use the Fabric from day one

Use `/layered` immediately if your pilot includes any of the following:

- risk acceptance or security exceptions;
- external exposure of a vulnerable or uncertain service;
- decisions requiring later auditability;
- situations where multiple competing options may need later defence.
## Public documentation and GitHub Releases

The public manual is built from the canonical `docs/` Markdown tree using
`mkdocs.yml` and `.github/workflows/pages.yml`. Configure **Settings → Pages →
Build and deployment → GitHub Actions** in the GitHub repository. The Pages
environment should permit deployment from `main` only. The existing Pages
workflow builds pull requests for validation but deploys only `main`.

The **Get Started**, **Download JAI**, and **View on GitHub** links are authored
in `docs/index.md` and styled in `docs/assets/stylesheets/enterprise.css`.
MkDocs replaces only the repository token within the two source-authored URLs at build time using the
canonical repository name (`GITHUB_REPOSITORY` in Actions, or
`JAI_GITHUB_REPOSITORY=owner/JAI` when building locally outside a Git clone).
No post-build HTML injection is performed. The download link deliberately opens
the repository's **Releases** page: that route remains valid before the first
public release, whereas `/releases/latest` would return 404.

Local preview from an unpacked release (without a Git remote):

```sh
JAI_GITHUB_REPOSITORY=YOUR_OWNER/JAI python -m mkdocs build --strict
```

For the current procedure, use [Versioning and release policy](../reference/versioning.md).
The root `VERSION` is the single authority; `.ai/VERSION` and
`.ai/runtime/VERSION` are projections, not independent authorities.
Synchronise them with
`scripts/versioning.py sync`, check and commit the consistent state, then
create a matching release tag. The workflow checks that committed identity
and the tag's ancestry in `main`; it does not derive a new version from the
tag. Publication requires the current qualification checks to succeed.

For an eligible public repository GitHub generates signed OIDC/Sigstore
attestations for the ZIP. On private GitHub plans without attestations the
release is still published with a SHA-256 checksum and embedded evidence;
this does **not** constitute a cryptographically signed provenance claim.
Protect `release@*` tags and use branch protection on `main`. GitHub Pages
is public where permitted, so assess documentation classification.

# Releases

## Automation

This project uses [semantic-release](https://semantic-release.gitbook.io/semantic-release) to automate versioning and deployment. The release process is triggered automatically when changes are merged into the `main` branch.

### Versioning

Semantic versioning is determined by the commit message prefix, examples include

- `feat:` for new features (minor version bump)
- `fix:` for bug fixes (patch version bump)
- `chore:` for maintenance tasks (no version bump unless files like dependencies are updated)
- `major:` for breaking changes (major version bump)

### Deployment

On every merge to `main`, the following occurs:

- The semantic version is updated based on commit messages.
- The `pyproject.toml` version is updated automatically to match the new release version.
- The package is deployed and released.

No manual intervention is required for versioning or deployment as long as commit messages follow the semantic-release convention.

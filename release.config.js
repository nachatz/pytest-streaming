module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    "semantic-release-pypi",
    [
      "@semantic-release/git",
      {
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}",
        "assets": [
          "pyproject.toml"
        ]
      }
    ],
    [
      '@semantic-release/github',
      {
        successComment: false,
        failComment: false,
      },
    ],
  ],
};
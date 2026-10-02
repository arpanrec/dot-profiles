module.exports = {
    branches: ['master'],
    tagFormat: '${version}',
    plugins: [
        [
            '@semantic-release/commit-analyzer',
            {
                preset: 'angular',
                parserOpts: {
                    noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
                },
            },
        ],
        [
            '@semantic-release/release-notes-generator',
            {
                preset: 'angular',
                parserOpts: {
                    noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
                },
                writerOpts: {
                    commitsSort: ['subject', 'scope'],
                },
            },
        ],
        [
            '@semantic-release/exec',
            {
                prepareCmd: [
                    'uv version ${nextRelease.version}',
                    'uv export --format requirements.txt --no-hashes --no-annotate --no-header --no-progress -o requirements.txt',
                    'uv export --format requirements.txt --no-hashes --no-annotate --no-header --no-progress --group dev -o requirements-dev.txt',
                    'uv build',
                    'uv run typer src/dot_profiles/__main__.py utils docs --output docs/cli.md',
                    `uv publish --index test-pypi --token ${process.env.PYPI_TEST_API_TOKEN}`,
                ].join(' && '),
                successCmd: `uv publish --index pypi --token ${process.env.PYPI_PROD_API_TOKEN}`,
            },
        ],
        '@semantic-release/github',
        [
            '@semantic-release/changelog',
            {
                changelogFile: 'CHANGELOG.md',
            },
        ],
        [
            '@semantic-release/git',
            {
                assets: [
                    'CHANGELOG.md',
                    'pyproject.toml',
                    'uv.lock',
                    'requirements.txt',
                    'requirements-dev.txt',
                    'docs/cli.md',
                    'README.md',
                ],
                message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
            },
        ],
    ],
};

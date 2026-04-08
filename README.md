# marketplace

[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

This repository is the data source for [Itential Marketplace](https://itential.com/marketplace). It aggregates metadata from community projects hosted on GitHub and adapters hosted on GitLab, and is not intended for general development use.

## How It Works

- **Community Projects** — Each project contributes a `metadata.yaml` file that describes the content, type, and metadata surfaced on the marketplace.
- **Adapters** — Adapter metadata is sourced from GitLab and referenced via `adapters.yaml`.

## Contributing

To contribute a project to the marketplace, see the [Contributing Guide](CONTRIBUTING.md). You'll also need to sign the [Contributor License Agreement](CLA.md).

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

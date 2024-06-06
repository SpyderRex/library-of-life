# library_of_life
`library_of_life` is a Python package that provides a client interface for interacting with the Global Biodiversity Information Facility (GBIF) API. The library is organized into submodules representing different APIs within the GBIF service, making it easy to access various resources related to biodiversity data.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Modules](#modules)
  - [Registry](#registry)
  - [Species](#species)
  - [Occurrence](#occurrences)
  - [Maps](#maps)
  - [Literature](#literature)
  - [Validator](#validator)
  - [Vocabulary](#vocabulary)
- [Caching](#caching)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install `library_of_life` via pip:

```bash
pip install library_of_life
```

## Quick Start

Here's a quick example to get you started with `library_of_life`:

```python
from library_of_life.registry.datasets import Datasets
from library_of_life.species.name_usage import NameUsage

# Initialize the Datasets and NameUsage classes
dataset_client = Datasets()
name_usage_client = NameUsage()

# List current datasets matching specified parameters
dataset = dataset_client.list_datasets(dataset_type="SAMPLING_EVENT", limit=10)
print(dataset)

# Return all vernacular species names by a specific usage key
vernacular_names= name_usage_client.get_usage_vernacular_names_by_usage_key(5231190)
print(vernacular_names)
```

## Modules

Each module is composed of separate submodules reflecting the divisions in the GBIF APIs. Within each of these submodules is a class and appropriate methods for accessing the data and resources available for the respective endpoints.

### Registry

For now the registry module only contains the principal methods, but it will be updated in the future to include all of the methods.

#### Submodules

- `datasets`
- `publishing_orgs`
- `participant_nodes`
- `networks`
- `tech_installations`
- `collections`
- `institutions`
- `institutions_and_collections`
- `derived_datasets`

### Species

#### Submodules

- `name_usage`
- `name_search`
- `name_parser`

### Occurrence

#### Submodules

- `single_occurrence`
- `search`
- `downloads`: (In development)
- `download_format`: (Pre-dev)
- `download_stats`: (Pre-dev)
- `metrics`: (Pre-dev)
- `inventories`: (Pre-dev)
- `gadm_regions`: (Pre-dev)
- `country_usages`: (Pre-dev)
- `organization_usages`: (Pre-dev)

### Maps (pre-dev)

### Literature (pre-dev)

### Validator (pre-dev)

### Vocabulary (pre-dev)

## Caching

Each class contains an optional caching feature using requests_cache. Simply set use_caching to True when initializing the respective class.

## Contributing

Contributions are welcome! If you would like to contribute to the development of `library_of_life`, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LCENSE](LICENSE) file for more details.I

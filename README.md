# generate-cf-params-file
Generate pseudo CloudFormation parameters file using Python

# Purpose

This Python script discovers CloudFormation files written in YAML and builds a parameters file for them based on CloudFormation parameter `Default:`, `AllowedValues:` and `Type:`.

## Order of precedence

> TL;DR: `Default` > `AllowedValues` > `Type`

When `Default` is provided, the `Default` is used.

When `Default` is not provided, it checks for `AllowedValues`  and picks a random value from the list of allowed values.

When `Default` and `AllowedValues` are not provided, the script generates a string of alphanumeric characters with the optional relevant prefixes based on the parameter `Type`.

> **Example:** For `AWS::EC2::Subnet::Id`, the script generates a string of `alphabets` with a prefix of `subnet-`. For more information, refer to `generate_value_for_parameter_type()` function within `parameter_type_handler/parameter_type_handler`.

# Configuration

| `config.json` file | Config as Environment variable(s) | Description |
|---------------|-----------------------------|-------------|
| `exclude_folders` | `exclude_folders` | In JSON, this value is a `list` of folder names. As an environment variable, please use a `comma-separated values`, like `jenkins,ansible`. The folder names found within `exclude_folders` will be skipped and the remaining YAML files will be parsed for Parameters within them and pseudo values would be generated for the same |

# Compatibility

| Language | Status |
|-------|------|
| `YAML` | :white_check_mark: |
| `JSON` | :x: |

# Future development

| Next Steps | Status |
|-------|------|
| GitHub Action | :construction: |
| Visual Studio Extension | :construction: |

# Issues?

For any issues or errors with this script, please raise an [issue here](https://github.com/GeorgeDavis-Ibexlabs/generate-cf-params-file/issues)

# Contribute

If you encounter a bug or think of a useful feature, or find something confusing in the docs, please create a new issue.

I ♥️ pull requests. If you'd like to fix a bug or contribute to a feature or simply correct a typo, please feel free to do so.

If you're thinking of adding a new feature, consider opening an issue first to discuss it to ensure it aligns with the direction of the project and potentially save yourself some time.
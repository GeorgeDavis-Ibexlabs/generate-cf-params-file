# generate-cf-params-file

Generate pseudo CloudFormation parameters file using Python

Project Status: **In Active Development**

# Purpose

This Python script discovers CloudFormation files written in YAML and builds a parameters file for them based on CloudFormation parameter `Default:`, `AllowedValues:` and `Type:`.

# Usage

1. Run Docker container using
`docker run --network host -itd generate-cf-params-file:latest`
2. (Optional) If you would like to alter the behaviour of the CloudFormation parser, copy the `config.json.example` file into `config.json`. For more information on the configuration variables available to you, refer the Configuration section of the documentation.

## Configuration

| `config.json` file | Config as Environment variable(s) | Description |
|---------------|-----------------------------|-------------|
| `exclude_folders` | `exclude_folders` | In JSON, this value is a list of folder names. As an environment variable, please use a comma-separated value, like `jenkins,ansible`. The folder names foud within `exclude_folders` will be skipped and the remaining YAML files will be parsed for Parameters within them and pseudo values would be generated for the same |

# Tool Compatibility

| Language | Status |
|-------|------|
| `json` | :white_check_mark: |
| `yaml` | :white_check_mark: |

# Future development

| Next Steps | Status |
|-------|------|
| GitHub Action | :white_check_mark: |
| Visual Studio Extension | :construction: |

## GitHub Actions

```
    - name: Generate pseduo CloudFormation Parameters file 
      uses: GeorgeDavis-Ibexlabs/generate-cf-params-file@v0.0.1
```
Refer to [Generate CloudFormation Parameters file using GitHub Actions](https://github.com/marketplace/actions/generate-cf-params-file)

## Work in progress 

- #### VSCode Extension

    Plans to build this project into a VSCode extension to generate local cf-params.json file direct from the IDE

# Issues?

For any issues or errors with this script, please raise an [issue here](https://github.com/GeorgeDavis-Ibexlabs/generate-cf-params-file/issues)

# Contribute

If you encounter a bug or think of a useful feature, or find something confusing in the docs, please create a new issue.

I ♥️ pull requests. If you'd like to fix a bug or contribute to a feature or simply correct a typo, please feel free to do so.

If you're thinking of adding a new feature, consider opening an issue first to discuss it to ensure it aligns with the direction of the project and potentially save yourself some time.

## Development

```sh
docker login
```

```sh
docker build --no-cache --progress=plain . -f Dockerfile -t generate-cf-params-file:latest 2>&1 | tee build.log
```

```sh
docker run --network host -itd \
-e LOG_LEVEL='DEBUG' \
generate-cf-params-file:latest
```

> Use log levels available within the Python `logging` library as values for `LOG_LEVEL`
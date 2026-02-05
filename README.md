# MSI Examples

A Poetry-managed Python project with data science dependencies.

## Dependencies

- **numpy**: Numerical computing library
- **pandas**: Data manipulation and analysis
- **ipython**: Interactive Python shell (dev dependency)

## Setup

Install dependencies using Poetry:

```bash
poetry install
```

To add a new dependency:

```bash
poetry add <package-name>
```

To add a dev dependency:

```bash
poetry add -G dev <package-name>
```

## Running Code

Use Poetry to run Python scripts:

```bash
poetry run python your_script.py
```

Or activate the virtual environment:

```bash
poetry shell
```

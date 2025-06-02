# pysits

Python wrapper for the [sits](https://github.com/e-sensing/sits) R package.

## 📦 Installation

To install `pysits` with pip:

```bash
pip install pysits
```

or the development version:

```bash
pip install git+https://github.com/e-sensing/pysits.git
```

## 🛠 Development setup (for contributors)

To set up a local development environment:

**1.** Clone the repo and access it:

```bash
git clone https://github.com/e-sensing/pysits.git
cd pysits
```

**2.** Create a virtual environment using [uv](https://github.com/astral-sh/uv)

```bash
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

**3.** Install the project in editable mode with development tools:

```bash
uv pip install -e ".[dev]"
```

### 🔍 Run tests

We use `pytest` for testing:

```bash
pytest
```

### 🧹 Code formatting

To keep the codebase clean and consistent we use [ruff](https://github.com/astral-sh/ruff):

```bash
ruff format .
```

### 🧪 Linting

We use [ruff](https://github.com/astral-sh/ruff) for static analysis:

```bash
ruff check .
```

> The `examples/` directory is excluded from linting.

## 📚 Learn more

Explore the [examples](./examples) directory for usage demos and tutorials.

## 🤝 Contributing

We welcome contributions! Please:

- Fork the repository
- Create a feature branch
- Submit a pull request with a clear description

## 📄 License

`pysits` is distributed under the GPL-2.0 license. See [LICENSE](./LICENSE) for more details.

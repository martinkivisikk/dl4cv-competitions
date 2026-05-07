# Setup

```bash
git clone https://github.com/martinkivisikk/dl4cv-competitions.git
cd dl4cv-competitions
```

Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

By default torch is installed for **AMD ROCm 7.2**. To change hardware target, edit the index URL in `pyproject.toml` before syncing:

| Hardware | URL |
|----------|-----|
| AMD ROCm 7.2 (default) | `https://download.pytorch.org/whl/rocm7.2` |
| NVIDIA CUDA 12.6 | `https://download.pytorch.org/whl/cu126` |
| CPU only | `https://download.pytorch.org/whl/cpu` |

Install dependencies

```bash
uv sync
```

Add your Kaggle API token

```bash
cp .env.example .env
```

Start Jupyter

```bash
jupyter lab
```

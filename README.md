# Setup

```bash
git clone https://github.com/martinkivisikk/dl4cv-competitions.git

cd dl4cv-competitions
```

Install uv

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Virtual env and dependencies
```bash
uv venv venv

source venv/bin/activate

# Install correct torch
# CUDA 12.6
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

# ROCm 7.2
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm7.2

# CPU
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Other deps
uv pip install kaggle numpy pandas tqdm python-dotenv ultralytics scikit-learn
```

Create .env and add your Kaggle API token
```bash
cp .env.example .env
```
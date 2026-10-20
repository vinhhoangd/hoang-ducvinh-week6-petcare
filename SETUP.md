# Week 6 setup (each teammate, once, on your own machine)

1. Clone: `git clone https://github.com/vinhhoangd/hoang-ducvinh-week6-petcare.git`
2. Install uv (Mac: `brew install uv`; Ubuntu: see https://docs.astral.sh/uv/getting-started/installation/).
3. In `project-workspace/`, create the project's own Python environment with the tested versions:
   ```bash
   uv venv --python 3.14 .venv
   uv pip install --python .venv/bin/python -r requirements.txt
   source .venv/bin/activate
   ```
   Check: `python3 -c "import pandas, sklearn; print('pandas', pandas.__version__, 'scikit-learn', sklearn.__version__)"` prints `pandas 3.0.6 scikit-learn 1.9.1`.
4. Research owner (and anyone running the skill): `uv tool install notebooklm-mcp-cli`, then `nlm --version` (0.15.6), then `nlm login` **yourself** in your own terminal.
5. Your own Census key: request it at https://api.census.gov/data/key_signup.html and type it yourself with `nano .env` in `project-workspace/` as one line `CENSUS_API=...`. Never paste it into an agent, chat, or file you share. `.env` is git-ignored.
6. Each work session: `cd project-workspace && source .venv/bin/activate && set -a; . ./.env; set +a`

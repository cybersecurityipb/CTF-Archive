# Repository Guidelines

## Challenge Overview
- Model: 32x32 matrix `A` over GF(2) with state update `S[n+1] = A * S[n] XOR B`; keystream bytes are the lowest byte of each 32-bit state.
- Goal: reconstruct `A`, derive `B`, and decrypt the captured ciphertext using leaked states and keystream bytes.
- Artifacts: ciphertext, keystream leaks, and this description from the challenge author (DJ Strigel).

## Project Structure & Module Organization
- Challenge artifacts live at the root: `cipher.txt`, `keystream_leak.txt`, and `README.txt` describing the task. Treat these as read-only fixtures.
- Place solver code in a dedicated folder such as `src/` (library-style functions) and `scripts/` (CLI entry points). Keep exploratory work in `notebooks/` or `notes/` to avoid mixing with reusable code.
- Store generated outputs (recovered matrices, plaintext) in `out/` or `tmp/` and add them to `.gitignore` before committing.

## Build, Test, and Development Commands
- No build system is required yet; run Python modules or scripts directly: `python3 scripts/solve.py --cipher cipher.txt --states keystream_leak.txt`.
- For dependencies, prefer a virtualenv: `python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.txt` (add the requirements file if you introduce third-party packages).
- Run tests with `pytest` from the repository root: `pytest -q`. Add a `conftest.py` for shared fixtures when the test suite grows.

## Coding Style & Naming Conventions
- Target Python 3.10+ with 4-space indentation and type hints on public functions. Use `__main__` guards for executable scripts.
- Favor pure, side-effect-light helpers (e.g., `reconstruct_matrix`, `apply_keystream`) and keep I/O at the script layer.
- Use `snake_case` for functions/variables, `PascalCase` for classes, and clear module names (`gf2.py`, `state_model.py`) for finite field utilities.
- If formatting is needed, apply `python -m black .` and lint with `python -m ruff .` (add configs when introduced).

## Testing Guidelines
- Create deterministic fixtures: small GF(2) matrices with known transitions and sample keystream slices. Keep them under `tests/fixtures/`.
- Name tests after behavior, e.g., `test_reconstruct_matrix_handles_singular_input`.
- Aim to cover edge cases: singular matrices, short/long state sequences, and corrupted keystream entries. Include at least one end-to-end decrypt test when possible.

## Commit & Pull Request Guidelines
- Write imperative, concise commit messages (e.g., `add gf2 helpers for state transition`). Mention relevant files or behaviors changed.
- For PRs, include: purpose/approach, commands run (tests/linters), and notes on data handling (e.g., artifacts untouched, new outputs in `out/`).
- Add screenshots or logs only when they clarify decrypted output or test coverage; avoid committing large generated files.

## Security & Data Integrity
- Do not edit or replace the provided ciphertext or keystream files; use copies for experimentation.
- Keep any recovered flags or secrets out of version control. Store environment-specific keys in `.env` files that stay untracked.

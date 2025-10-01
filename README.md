# Crew Estimator

[![CI](https://github.com/israellopezdeveloper/crew_estimator/actions/workflows/ci.yml/badge.svg)](https://github.com/israellopezdeveloper/crew_estimator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/israellopezdeveloper/crew_estimator/badge.svg?branch=main)](https://coveralls.io/github/israellopezdeveloper/crew_estimator?branch=main)

A small Python package that estimates the required moving crew size
based on volume, bulky items, stairs, and distance.  
This project is managed with **Poetry** and includes a full QA setup:
`pytest`, `hypothesis`, `mypy`, `ruff` and `black`.

## Functionality

The core function is:

```python
def estimate_crew(
    volume_cuft: float,
    bulky_count: int,
    stair_flights: int,
    long_distance: bool
) -> int:
    ...
```

### Rules

- Start with **2 crew members**.
- If `volume_cuft > 480`, add **+1 crew**.
- For every **2 bulky items**, add **+1 crew**:
  - 0–1 bulky items → +0
  - 2–3 bulky items → +1
  - 4–5 bulky items → +2

- If `stair_flights >= 3`, add **+1 crew**.
- If `long_distance is True`, add **+1 crew**.

### Example

```python
>>> from crew_estimator.estimator import estimate_crew
>>> estimate_crew(550, 3, 2, False)
4
```

## Testing

### Unit & Edge Tests

- Validate correct output for edge conditions (volume thresholds,
  bulky item thresholds, stairs cutoff).
- Include invalid inputs (negative values, wrong types, NaN/Infinity).

### Property-Based Tests (Hypothesis)

- Automatically generate thousands of cases.
- Ensure:
  - Function matches the specification model.
  - Monotonicity: increasing inputs never decreases crew.
  - Step-function behavior for bulky items.
  - `long_distance=True` always adds exactly +1.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/israellopezdeveloper/crew_estimator.git
   cd crew_estimator
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

## Running Tests

Run the full test suite:

```bash
poetry run pytest
```

Run Hypothesis tests with statistics (development profile):

```bash
make check-stats-dev
```

Run Hypothesis tests with stricter settings (CI profile):

```bash
make check-stats-ci
```

## Quality Assurance

The project includes a `Makefile` to simplify linting, formatting, and
type checking.

- Run linting (Ruff):

  ```bash
  make lint
  ```

- Run formatter (Black):

  ```bash
  make format
  ```

- Run type checking (mypy):

  ```bash
  make typecheck
  ```

- Run **all checks** (lint, format, typecheck):

  ```bash
  make qa
  ```

- Run tests:

  ```bash
  make check
  ```

## Development Dependencies

- [pytest](https://docs.pytest.org/) – unit testing framework
- [hypothesis](https://hypothesis.readthedocs.io/) – property-based
  testing
- [mypy](http://mypy-lang.org/) – static type checker
- [ruff](https://docs.astral.sh/ruff/) – fast Python linter
- [black](https://black.readthedocs.io/) – code formatter

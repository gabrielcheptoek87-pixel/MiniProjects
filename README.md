markdown

# Ugandan Context Mini-Projects: Simulation & Modeling

This repository contains a collection of mini-projects focused on data modeling, simulation, and analysis within various Ugandan economic, environmental, and social contexts. Each project is implemented as an independent, reproducible Jupyter Notebook supported by a robust, object-oriented Python codebase.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Conda](https://conda.io) (optional, but recommended for environment management)

### Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com
   cd https://github.com/gabrielcheptoek87-pixel/MiniProjects.git
   ```

2. **Set up the environment:**
   - **Using `pip`:**
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use: venv\Scripts\activate
     pip install -r requirements.txt
     ```
   - **Using `conda`:**
     ```bash
     conda env create -f environment.yml
     conda activate uganda-modeling-env
     ```

3. **Launch the Notebooks:**
   ```bash
   jupyter notebook
   ```

---

## 📂 Project Structure

The repository is modularized to separate reusable business logic from exploratory analysis and visual reporting.

```text
├── src/                      # Reusable python modules
│   ├── __init__.py
│   ├── population.py         # OOP Models for Population dynamics
│   ├── environment.py        # Environmental & UNMA weather simulators
│   └── finance.py            # Financial & Bank of Uganda economic models
├── notebooks/                # Production Jupyter Notebooks
│   ├── project1_population.ipynb
│   ├── project2_weather.ipynb
│   └── project3_finance.ipynb
├── tests/                    # Pytest unit testing suite
│   ├── test_population.py
│   ├── test_environment.py
│   └── test_finance.py
├── .gitignore
├── environment.yml           # Conda environment definition
├── requirements.txt          # Pip package dependencies
└── README.md                 # Project documentation
```

---

## 🏗️ Core Software Architecture

To enforce clean software engineering principles, every mini-project models its specific domain using explicit **Object-Oriented Programming (OOP)** rules:

- **Type Hinting & Docstrings:** All methods and classes use strict PEP 484 type hints and descriptive Google-style docstrings.
- **Deterministic Reproducibility:** Random processes utilize localized random generators (`numpy.random.default_rng(seed)`) to ensure that executing **Restart & Run All** yields identical results across any machine.
- **Encapsulation:** Mathematical formulas and tracking states are bound to class properties and methods, avoiding global variables.

---

## 🧪 Testing Suite

Automated testing is handled via `pytest`. Each mini-project includes at least three test cases covering structural data outputs and protective error limits.

### Running Tests

Execute the following command from the root directory to run all unit tests:

```bash
pytest
```

Our testing patterns validate:

1. **Happy Path:** Expected operations given normal Ugandan environmental or economic parameters.
2. **Boundary Constraints:** Expected behavior under values such as `0` or near-infinite scaling limits.
3. **Edge Cases & Error Handling:** Proper execution of exceptions when handed empty sequences or invalid inputs (e.g., negative population counts or impossible interest rates).

---

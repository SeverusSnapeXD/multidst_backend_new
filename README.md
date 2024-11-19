# MultiDST Backend API

This is a backend API for analyzing p-values using the MultiDST framework. The API is built with **FastAPI**, allowing for scalable and efficient handling of requests. It includes endpoints for computing results with multiple hypothesis testing methods and generating visualizations of p-value distributions and significance indices.

---

## Features

- Analyze p-values using multiple hypothesis testing methods:
  - Bonferroni
  - Holm
  - SGoF
  - BH (Benjamini-Hochberg)
  - BY (Benjamini-Yekutieli)
  - Storey's Q-value
- Generate visualizations:
  - Histogram of p-values
  - Significant Index Plot (SIP)
- Cross-Origin Resource Sharing (CORS) enabled for flexible integration.
- Static file serving for generated visualizations.

---

## Requirements

- Python 3.9 or later
- Dependencies listed in `requirements.txt` or install the following manually:
  - `fastapi`
  - `uvicorn`
  - `pydantic`
  - `multidst` (Custom library for hypothesis testing)

---


## Running the Application
```bash
python -m uvicorn main:app --reload
```
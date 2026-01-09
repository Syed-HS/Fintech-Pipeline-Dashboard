# 🎛️ FinTech Pipeline Live Audit Dashboard

An enterprise-grade, high-density compliance telemetry platform built with Streamlit. This application acts as a real-time validation, auditing, and anomaly mitigation bridge for streaming financial transactions.

---

## 🎨 Design System & Palette
The interface utilizes a custom high-contrast executive dark profile accented by structured palette parameters:
* **Soft Blossom** (`#e9b7ce`) – Batch Ingestion Volume indicators & chart series.
* **Lavender** (`#ded5e0`) – Pipeline Success Rate metrics.
* **Frozen Water** (`#d3f3f1`) – Quarantine Queue tracking modules.

---

## 🔒 Core Architecture Features

### 1. Gatekeeper Security Layer
* **PIN Authentication:** The dashboard is protected by an immediate institutional state block (`SECURE_AUDIT_PIN = "4321"`).
* **Execution Isolation:** Utilizes script-level hard halts (`st.stop()`) to ensure no downstream data loops, database operations, or metrics are computed or leaked prior to authorization.

### 2. High-Density Viewport Optimization
* **Single-Screen Layout:** Engineered to sit entirely within a standard 1080p workspace with zero page scrolling.
* **Compact Control Center:** Interactive sidebar controls use side-by-side widget placement (date/time pickers and transaction metadata inputs) to prevent form overflowing.

### 3. Contextual Data Telemetry
* **Proactive Metrics Engine:** Evaluates and highlights execution trends (e.g., Success Rates, Volumetric Changes) leading with clear percentages rather than raw database logs.
* **7-Day Historical Benchmarks:** Compares active batches directly against trailing baseline numbers to immediately spot ingestion spikes.
* **Risk-Aligned Alerts:** Color logic automatically sets storage tracking parameters to critical/warning states if queues are stagnating while backlogs exist.
* **Spreadsheet Drill-Downs:** Provides an on-demand raw interactive viewer into quarantined blocks with single-click expansion.

---

## 🛠️ Operational Setup

### Prerequisites
* Python 3.10+
* PostgreSQL Database instance (with local SQLite auto-fallback protection)

### Installation
1. Clone the repository and navigate into the workspace directory:
   ```bash
   cd fintech-pipeline

2. Initialize and activate your virtual environment:
    ```bash
    # On Windows (PowerShell):
     .\venv\Scripts\Activate.ps1
    # Mac/Linux: source venv/bin/activate

3. Install required runtime dependencies:
    ```bash
      pip install streamlit pandas numpy sqlalchemy psycopg2-binary altair

4. Running the Application (Launch the local network instance using Streamlit)

    ```bash
      streamlit run dashboard.py

5.  Git Configuration : (The project is versioned cleanly on GitHub, ignoring virtual environments, runtime file footprints, and temporary SQLite databases via standard .gitignore formatting rules:)

   ```bash

    git add .
    git commit -m "feat: implement high-density secured fintech audit dashboard"
    git push
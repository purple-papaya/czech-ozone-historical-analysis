# 🇨🇿 Czech Ozone Historical Analysis

## 🎯 Business Impact
Providing accessible historical ozone pollution analysis to help Czech citizens, researchers, and policymakers understand air quality trends and make informed health decisions during high pollution episodes.

## 📊 Project Overview
Comprehensive tracking and analysis of ground-level ozone pollution trends across Czech Republic's environmental monitoring network

### 📋 About This Project
Ground-level ozone (O₃) is a major air pollutant that affects human health, vegetation, and ecosystems. This project analyzes historical ozone concentration data from the Czech Hydrometeorological Institute (CHMI) to understand:

* Temporal trends: How ozone levels have changed over the years
* Seasonal patterns: When and why ozone concentrations peak
* Regional variations: Which areas of Czech Republic experience the highest pollution
* Health implications: When ozone levels exceed EU safety thresholds

### Why Ozone Matters
Unlike other air pollutants, ozone is not directly emitted but forms through photochemical reactions between nitrogen oxides and volatile organic compounds in the presence of sunlight. This makes it particularly problematic during warm, sunny summer months. High ozone concentrations can cause:

* Respiratory problems and reduced lung function
* Aggravation of asthma and other lung diseases
* Damage to crops and forest ecosystems
* Reduced visibility and environmental degradation

## 🚀 Quick Start
```bash
# Clone this repository
git clone https://github.com/purple-papaya/czech-ozone-historical-analysis.git
cd czech-ozone-historical-analysis

# Option 1: Use setup script (installs UV if needed)
./setup.sh                      # Linux/Mac
# setup.bat                     # Windows

# Option 2: Manual setup with UV
uv sync                         # Install dependencies
source .venv/bin/activate       # Activate environment (Linux/Mac)
# .venv\Scripts\activate        # Activate environment (Windows)

# Download CHMI data (see Data Sources section)

# Start analysis with Jupyter (traditional)
uv run jupyter notebook

# Or use Marimo (reactive, modern - cells auto-update!)
uv run marimo edit

# Or use Make commands
make install      # Install dependencies
make notebook     # Start Jupyter
make marimo       # Start Marimo
make test         # Run tests
```

## 📁 Project Structure

```bash
czech-ozone-historical-analysis/
├── pyproject.toml              # Project config & dependencies (UV)
├── uv.lock                     # Lock file for reproducibility
├── .python-version             # Python version (3.10)
├── Makefile                    # Development commands
├── data/
│   ├── raw/                    # Original CHMI CSV files
│   ├── interim/                # Intermediate transformations
│   ├── processed/              # Final datasets for analysis
│   └── external/               # Third-party data
├── notebooks/                  # Jupyter & Marimo notebooks
│   └── archive/                # Old experiments
├── src/                        # Source code
│   ├── data/                   # Data ingestion & cleaning
│   ├── features/               # Feature engineering
│   ├── models/                 # Statistical models
│   └── visualization/          # Plotly chart templates
├── models/                     # Saved models/analysis
├── reports/                    # Generated analysis
│   └── figures/                # Visualizations
├── tests/                      # Unit tests
└── README.md                   # This file
```

## 🔧 Technologies Used

* Package Manager: UV (fast Python package manager)
* Data Processing: Pandas, Polars (fast DataFrame operations)
* Machine Learning: Scikit-learn
* Visualization: Matplotlib, Seaborn, Plotly
* Notebooks: Jupyter (traditional), Marimo (reactive)
* Environment: Python 3.10+

## 💻 Development Commands

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev

# Install with all extras (notebooks, visualization, ML)
uv sync --extra all

# Start Jupyter (traditional notebook)
uv run jupyter notebook

# Start Marimo (reactive notebook - automatically re-runs cells!)
uv run marimo edit

# Create new Marimo notebook
uv run marimo new notebooks/05-initials-your-analysis.py

# Run main analysis
uv run python src/main.py

# Run tests
uv run pytest tests/ -v

# Format code
uv run ruff format src/ tests/

# Check code quality
uv run ruff check src/

# Or use Make commands for convenience
make help           # Show all available commands
make install        # Install dependencies
make install-dev    # Install with dev dependencies
make notebook       # Start Jupyter
make marimo         # Start Marimo editor
make marimo-new name=my-analysis    # Create new Marimo notebook
make marimo-run name=my-analysis    # Run Marimo as web app
make test           # Run tests
make lint           # Check code quality
make format         # Format code
make clean          # Clean build artifacts
```

## 📚 Data Sources

### Primary Data: CHMI OpenISKO Portal
The Czech Hydrometeorological Institute provides historical air quality data through their **OpenISKO portal**:

🔗 **Main Data Portal**: [CHMI Historical Data](https://www.chmi.cz/files/portal/docs/uoco/historicka_data/OpenIsko_data/index.html)

Data characteristics:

* Time coverage: 1969 - present
* Temporal resolution: Hourly measurements
* Pollutants: O₃ (ozone), plus NO₂, SO₂, PM10, and other pollutants
* Units: µg/m³ (micrograms per cubic meter)
* Format: CSV files organized by station code
* Stations: 198 monitoring stations across Czech Republic

Key monitoring stations:

* TOPOM - Ostrava-Poruba (industrial region)
* ALIBM - Praha 4-Libus (urban background)
* BBRUA - Brno-Tuřany (regional city)
* Many rural and mountain stations for background measurements

### Additional Resources

* 📖 CHMI Air Quality Portal: https://www.chmi.cz/aktualni-situace/stav-ovzdusi
* 🇪🇺 EU Air Quality Standards: [European Environment Agency](https://www.eea.europa.eu/themes/air/air-quality-concentrations/air-quality-standards)
* 📊 WHO Air Quality Guidelines: [WHO Guidelines](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)
* 🌍 Real-time Czech AQ Index: [AQICN Czech Republic](https://aqicn.org/city/czechrepublic/)

## 🌟 Why Polars?

Polars is used alongside Pandas for:

* ⚡ 10x faster operations on large CHMI datasets
* 🔄 Lazy evaluation - optimizes query plans automatically
* 💾 Better memory usage - handles decades of hourly data efficiently
* 🎯 Similar API to Pandas - easy to learn

Perfect for processing years of hourly ozone measurements from 198+ monitoring stations!

## 🎨 Why Marimo?

Marimo is included alongside Jupyter for:

* 🔄 Reactive execution - cells auto-update when data changes
* 🐛 No hidden state - prevents common notebook bugs
* 🚀 Runs as scripts - notebooks are just Python files
* 🎯 Git-friendly - clean diffs, easy versioning
* 📱 Interactive apps - deploy analyses as web apps

Perfect for exploring ozone trends interactively!

## 📝 Next Steps

1. ✅ Clone the repository and run ./setup.sh
2. 📥 Download CHMI historical data for your regions of interest

## 👤 Author
@purple-papaya - [LinkedIn](https://www.linkedin.com/in/pauline-novak/)

**Note**: This is an educational and research project. For official air quality information and health advisories, please consult [CHMI's official portal](https://www.chmi.cz/).

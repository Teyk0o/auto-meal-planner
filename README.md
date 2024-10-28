# 🍽️ Auto Meal Planner ![Tests](https://github.com/teyk0o/auto-meal-planner/actions/workflows/test.yml/badge.svg)

> 🤖 AI-powered meal planning and shopping list generator based on real-time supermarket prices.

## 🌟 Features

- 📊 Smart processing of supermarket product data
- 💰 Real-time price analysis and optimization
- 🗓️ AI-generated personalized meal plans
- 🛒 Automated shopping list generation
- 📈 Data visualization and analytics

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Conda environment
- PyCharm (recommended)

### 🛠️ Installation

1. Clone the repository
```bash
git clone https://github.com/Teyk0o/auto-meal-planner.git
cd auto-meal-planner
```

2. Create and activate conda environment
```bash
conda create -n meal-planner python=3.12
conda activate meal-planner
```

3. Install dependencies
```bash
pip install -e .
```

## 📝 Usage

1. Place your raw CSV data in `data/raw/`
2. Run the data processor:
```python
from src.processors.csv_processor import CSVProcessor
processor = CSVProcessor("data/raw/input.csv")
df = processor.process_csv()
```

3. Explore the data using Jupyter notebooks in `notebooks/`

## 🔬 Project Structure

```
auto-meal-planner/
├── src/               # Source code
├── data/              # Data files
│   ├── raw/          # Raw input data
│   └── processed/    # Processed output data
├── notebooks/        # Jupyter notebooks
├── tests/           # Unit tests
└── docs/            # Documentation
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📊 Data Analysis

Explore the processed data using Jupyter notebooks:
1. Open PyCharm
2. Navigate to `notebooks/`
3. Run the analysis notebooks

## 🤝 Contributing

This project is for personal use only. See LICENSE for details.

## 📜 License

This project is licensed under a custom restrictive license - see the [LICENSE](LICENSE) file for details.

## ✨ Acknowledgments

- Created by Théo Vln / Teyk0o
- Built with Python and Google's Gemini API
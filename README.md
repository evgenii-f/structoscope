# Structoscope

**Structoscope** is an interactive data analysis tool for exploring materials simulation datasets.  
It provides convenient widgets and plotting panels to filter, categorize, and visualize structural data, including forces, magnetic moments, and energies.

## Features

- ✅ Interactive category selection panel
- ✅ Filtering by physical quantities (energy, volume, force, magnetism, etc.)
- ✅ Dynamic 2D/3D plotting (matplotlib and plotly)
- ✅ Modular and extensible design
- ✅ Notebook-ready components

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/evgenii-f/structoscope.git
cd structoscope
pip install -r requirements.txt
```
Make sure you have Jupyter or JupyterLab installed for interactive use:

```bash
pip install jupyterlab  # optional
```

## Usage

Open the example notebook ```analysis_example.ipynb```

Or create your own by importing the ```widgets``` and ```utils``` modules.

## Project Structure

```
structoscope/
├── widgets/                   # Interactive panels (CategoryPanel, PlotPanel, SavePanel)
├── utils/                     # Helper functions (text cleaning, plotting, etc.)
├── analysis_example.ipynb     # Example usage in a notebook
├── requirements.txt
└── README.md
```

## Development
This is an early-stage MVP developed for material data analysis. Feedback and contributions are welcome!
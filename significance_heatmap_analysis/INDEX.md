# Significance Heatmap Analysis

A complete, self-contained pipeline for analyzing emotional/trait response patterns across AI models and personality types.

## 🚀 Quick Start (30 seconds)

```bash
cd significance_heatmap_analysis

# Option 1: Simple bash runner
./run.sh

# Option 2: Direct Python
python3 significance_heatmap_pipeline.py

# View results in browser
open outputs/index.html
```

## 📁 What's Inside

This folder contains everything you need:

| File | Purpose |
|------|---------|
| **significance_heatmap_pipeline.py** | Main Python script (computes stats & generates plots) |
| **run.sh** | Bash runner (auto-installs dependencies) |
| **outputs/** | Generated results (10 PNG heatmaps + interactive HTML) |
| **README.md** | Complete documentation & reference |
| **STRUCTURE.md** | Folder organization guide |
| **INDEX.md** | This file |

## 📊 What Gets Generated

Running the pipeline creates:

1. **10 PNG Heatmaps** - One per emotion
   - Model × Personality grid
   - Statistical significance annotations
   - Confidence intervals & sample sizes
   - Publication-ready quality (150 DPI)

2. **Interactive HTML Dashboard** (`index.html`)
   - Click emotion cards to switch views
   - Table showing top 10 significant effects
   - Responsive design (desktop & mobile)
   - Emotion statistics sidebar

## 🔬 Statistical Method

- **Test**: One-sample t-test (A vs B)
- **Correction**: Benjamini-Hochberg FDR
- **Significance**: α = 0.05 (configurable)
- **Effect size**: Mean difference with 95% CI

## 🎯 Example Output

```
================================================================================
SUMMARY: APPROVAL
================================================================================
Total comparisons            : 77
Significant (FDR-corrected)  : 51
Correction method            : Benjamini-Hochberg FDR

Top 5 Most Significant Effects:
  qwen-32b-chat      × vlog              : Δ = -0.086 [-0.10, -0.07], p_adj = 8.407e-20
  qwen-8b-chat       × vlog              : Δ = -0.083 [-0.10, -0.07], p_adj = 3.054e-18
  ...
```

## 📖 Documentation

- **README.md** - Full documentation with:
  - Configuration options
  - Advanced usage examples
  - Troubleshooting guide
  - Data requirements

- **STRUCTURE.md** - Visual guide to folder organization

## ⚙️ Configuration

Edit `significance_heatmap_pipeline.py` to customize:

```python
CSV_PATH = Path(...)          # Input CSV location
OUTPUT_DIR = Path(...)        # Where to save outputs
ALPHA = 0.05                  # Significance threshold
EMOTIONS = [...]              # List of emotions to process
```

## 🐍 Requirements

- Python 3.7+
- Dependencies: pandas, numpy, scipy, matplotlib, seaborn, statsmodels

Auto-installed by `run.sh`, or manually:
```bash
pip3 install pandas numpy scipy matplotlib seaborn statsmodels
```

## 📂 Folder Structure

```
significance_heatmap_analysis/
├── significance_heatmap_pipeline.py   ← Main script
├── run.sh                             ← Runner script
├── README.md                          ← Full docs
├── STRUCTURE.md                       ← Folder guide
├── INDEX.md                           ← This file
└── outputs/                           ← Generated results
    ├── index.html                     ← Interactive dashboard ⭐
    ├── joy_heatmap.png
    ├── excitement_heatmap.png
    ├── confusion_heatmap.png
    ├── curiosity_heatmap.png
    ├── admiration_heatmap.png
    ├── approval_heatmap.png
    ├── caring_heatmap.png
    ├── nervousness_heatmap.png
    ├── optimism_heatmap.png
    └── surprise_heatmap.png
```

## ✨ Key Features

- ✅ **Self-contained** - Everything in one folder
- ✅ **Automated** - One command to regenerate
- ✅ **Interactive** - HTML dashboard for exploration
- ✅ **Publication-ready** - High-res PNG outputs
- ✅ **Well-documented** - Comprehensive guides
- ✅ **Configurable** - Easy to customize

## 🔄 Workflow

```
CSV Input
   ↓
Run pipeline
   ↓
Compute statistics
   ↓
Generate visualizations
   ↓
Create HTML dashboard
   ↓
View in browser
```

## 💡 Tips

- **To regenerate**: Just run `./run.sh` again
- **To modify settings**: Edit the `EMOTIONS` list or `ALPHA` in the Python script
- **To share results**: Send the entire `significance_heatmap_analysis/` folder
- **For details**: See README.md for comprehensive documentation

## 🆘 Need Help?

1. Check **README.md** for troubleshooting
2. Verify CSV path is correct
3. Ensure dependencies are installed: `pip3 install -r requirements.txt`
4. Check console output for specific error messages

---

**Ready to explore?** → Open `outputs/index.html` in your browser! 🎉

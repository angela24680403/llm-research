# Folder Structure

```
significance_heatmap_analysis/
├── README.md                              # Comprehensive documentation
├── run.sh                                 # Quick runner script (bash)
├── significance_heatmap_pipeline.py       # Main Python pipeline
└── outputs/
    ├── index.html                         # Interactive HTML dashboard ⭐
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

## Quick Start

### Option 1: Using the bash runner
```bash
cd significance_heatmap_analysis
./run.sh
```

### Option 2: Run directly with Python
```bash
cd significance_heatmap_analysis
python3 significance_heatmap_pipeline.py
```

### Option 3: View existing results
```bash
# Open the dashboard in your browser
open significance_heatmap_analysis/outputs/index.html
```

## File Descriptions

| File | Purpose |
|------|---------|
| **README.md** | Full documentation with configuration, advanced usage, and troubleshooting |
| **run.sh** | Bash script that installs dependencies and runs the pipeline |
| **significance_heatmap_pipeline.py** | Main Python script - computes stats and generates visualizations |
| **outputs/index.html** | Interactive web dashboard - click emotions to explore |
| **outputs/*.png** | 10 high-quality publication-ready heatmaps (one per emotion) |

## Key Features

✅ **Self-contained**: All files in one folder  
✅ **Automated**: Run `./run.sh` to regenerate results  
✅ **Interactive**: HTML dashboard for easy exploration  
✅ **Publication-ready**: High-resolution PNG outputs  
✅ **Well-documented**: Complete README with examples  
✅ **Configurable**: Easily modify emotions, significance level, output paths  

## Data Flow

```
Input: 7000_sampling_emotions.csv
         ↓
    [Python Pipeline]
         ↓
Output: 10 PNG heatmaps + HTML dashboard
```

The pipeline:
1. Loads CSV data
2. Computes statistics for each emotion
3. Applies FDR correction
4. Generates heatmaps with annotations
5. Creates interactive HTML dashboard

## Next Steps

1. **View results**: Open `outputs/index.html` in browser
2. **Read docs**: See `README.md` for detailed information
3. **Modify pipeline**: Edit `significance_heatmap_pipeline.py` to customize
4. **Regenerate**: Run `./run.sh` to recreate outputs anytime

## Requirements

- Python 3.7+
- pandas, numpy, scipy, matplotlib, seaborn, statsmodels

(Automatically installed by `run.sh`)

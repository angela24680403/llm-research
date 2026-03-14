# Significance Heatmap Pipeline

A comprehensive pipeline for computing statistical significance heatmaps across all 10 emotions and generating an interactive HTML dashboard for exploration.

## Quick Start

### Run the Pipeline

```bash
python3 significance_heatmap_pipeline.py
```

This will:
1. Load the CSV data (`7000_sampling_emotions.csv`)
2. Compute statistics for all 10 emotions
3. Generate high-quality PNG heatmaps
4. Create an interactive HTML dashboard
5. Display results in `generated_results/significance_heatmaps/`

### View Results

Open the generated HTML dashboard in your browser:
```
generated_results/significance_heatmaps/index.html
```

## What Gets Generated

### 1. PNG Heatmaps (one per emotion)
- **File format**: High-resolution PNG (150 DPI)
- **Content**: Model × Personality grid showing:
  - Mean difference (A − B) with color intensity
  - Significance stars (***) for FDR-corrected p < 0.05
  - 95% confidence intervals
  - Sample sizes per cell
  
Files:
- `joy_heatmap.png`
- `excitement_heatmap.png`
- `confusion_heatmap.png`
- `curiosity_heatmap.png`
- `admiration_heatmap.png`
- `approval_heatmap.png`
- `caring_heatmap.png`
- `nervousness_heatmap.png`
- `optimism_heatmap.png`
- `surprise_heatmap.png`

### 2. Interactive HTML Dashboard
- **File**: `index.html`
- **Features**:
  - Sidebar with emotion cards showing quick stats
  - Click any emotion to view its heatmap and top 10 most significant results
  - Responsive design works on desktop and mobile
  - Shows per-emotion statistics:
    - Number of significant effects
    - Maximum effect size
    - Coverage (% significant)

## Statistical Details

### Statistical Test
- **Method**: One-sample t-test on trait probability differences (A − B)
- **Null Hypothesis**: Mean difference = 0
- **Multiple Comparison Correction**: Benjamini-Hochberg FDR
- **Significance Level**: α = 0.05 (configurable)

### What Each Cell Shows
```
       ±0.xxx  ← Mean difference with significance stars (***)
[+/-0.xx, +/-0.xx]  ← 95% confidence interval
         n = XXXX   ← Sample size
```

### Color Scheme
- **Red**: Positive difference (Condition A > Condition B)
- **Blue**: Negative difference (Condition A < Condition B)
- **Intensity**: Magnitude of difference

## Configuration

Edit `significance_heatmap_pipeline.py` to customize:

```python
CSV_PATH = Path(...)          # Path to CSV file
OUTPUT_DIR = Path(...)        # Output directory
ALPHA = 0.05                  # Significance level
EMOTIONS = [...]              # List of emotion columns to process
```

## Data Requirements

The CSV must contain:
- `model` - AI model identifier
- `personality` - Personality type (neutral, school, reddit, linkedin, news, research, vlog)
- For each emotion: `{emotion}_prob_a` and `{emotion}_prob_b` columns

Example columns:
```
joy_prob_a, joy_prob_b
excitement_prob_a, excitement_prob_b
...
approval_prob_a, approval_prob_b
```

## Output Format

```
generated_results/significance_heatmaps/
├── index.html              # Interactive dashboard
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

## Key Functions

### `compute_statistics(df, trait_name, alpha=0.05)`
Computes t-test statistics with FDR correction for a single emotion.

**Returns**: DataFrame with columns:
- `model`, `personality`: Grouping variables
- `mean_diff`: Mean difference (A − B)
- `p_value`: Unadjusted p-value
- `p_adj`: FDR-adjusted p-value
- `ci_low`, `ci_high`: 95% confidence interval
- `n`: Sample size
- `significant`: Boolean (FDR-corrected p < α)

### `plot_significance_heatmap(results_df, trait_name, alpha=0.05, output_path=None)`
Generates a publication-quality heatmap with detailed annotations.

**Returns**: matplotlib figure (or saves to PNG if `output_path` specified)

### `generate_html_dashboard(results_dict, metadata, output_dir)`
Creates an interactive HTML dashboard for exploring all heatmaps.

**Returns**: Path to index.html

## Advanced Usage

### Process Only Specific Emotions
```python
EMOTIONS = ["joy", "approval", "curiosity"]
run_pipeline(CSV_PATH, OUTPUT_DIR, EMOTIONS)
```

### Change Significance Level
```python
ALPHA = 0.01  # More stringent
run_pipeline(CSV_PATH, OUTPUT_DIR, EMOTIONS, alpha=ALPHA)
```

### Custom Output Location
```python
OUTPUT_DIR = Path("/custom/output/path")
run_pipeline(CSV_PATH, OUTPUT_DIR, EMOTIONS)
```

## Console Output

The pipeline prints a summary table for each emotion:

```
================================================================================
SUMMARY: APPROVAL
================================================================================
Total comparisons            : 77
Significant (FDR-corrected)  : 51
Correction method            : Benjamini-Hochberg FDR
Significance level (α)       : 0.05

Top 5 Most Significant Effects:
--------------------------------------------------------------------------------
  qwen-32b-chat      × vlog              : Δ = -0.086 [-0.10, -0.07], p_adj = 8.407e-20
  qwen-8b-chat       × vlog              : Δ = -0.083 [-0.10, -0.07], p_adj = 3.054e-18
  ...
```

## Troubleshooting

### Missing module errors
Install dependencies:
```bash
pip3 install statsmodels seaborn matplotlib scipy pandas numpy
```

### File not found
Verify CSV path in script:
```bash
ls -la demo-notebooks/generated_results/7000_sampling_emotions.csv
```

### Permission denied
Check output directory permissions:
```bash
mkdir -p generated_results/significance_heatmaps
chmod 755 generated_results/significance_heatmaps
```

## Performance

On a typical machine with ~122K data rows:
- Processing time: ~2-3 minutes
- Output size: ~5 MB (10 PNG files + HTML)
- Memory usage: ~500 MB

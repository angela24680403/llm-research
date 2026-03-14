# Personality Distribution Analysis Dashboard

A research dashboard for analyzing how Large Language Models adopt different personalities across diverse contexts and use-cases.

## 🎯 Research Focus

**Core Question**: Are LLMs monolithic personality entities, or do they flexibly adopt different personality profiles?

**Hypothesis**: Models are not personality-singular. Instead, they:
- Demonstrate distinct emotional responses in different personality contexts
- Vary in how much they adapt personalities (consistency)
- Create measurable emotional "distance" between personalities (diversity)
- Show systematic differences based on training (base vs. chat, distilled vs. original)

## 📊 What Gets Generated

### 7 Publication-Ready Visualizations

1. **Personality Profiles by Model** (11-panel heatmap)
   - Shows how each model expresses emotions across all 7 personalities
   - Color intensity = emotion probability
   - Reveals per-model personality expression patterns

2. **Personality Consistency** (2-panel comparison)
   - Coefficient of Variation: How consistent is each model's emotion expression?
   - Mean Range: How much does personality affect emotional responses?
   - Green/Blue = consistent; Red/Orange = varies by personality

3. **Personality Diversity** (1-panel bar chart)
   - Measures Euclidean distance between personality profiles
   - Higher = more distinct personalities
   - Colored by model type (base/chat/distilled/MOE)

4. **Emotion Variability** (2-panel heatmap)
   - Which emotions change the most across personalities?
   - Coefficient of Variation vs. Standard Deviation
   - Identifies personality-responsive vs. personality-neutral emotions

5. **Model Type Comparison** (4-panel grid)
   - Separate heatmaps for: Base, Chat, Distilled, MOE models
   - Shows if training procedure affects personality expression
   - Base vs. Chat comparison reveals RLHF effects

6. **Model Generation Comparison** (2-panel plot)
   - Line plot: Emotions by model size (8B, 32B, 70B)
   - Bar plot: Aggregated statistics by generation
   - Reveals scaling effects on personality

7. **Personality Radar Charts** (7-panel polar plots)
   - Unique emotional signature for each personality type
   - Shows personality archetypes in emotional space
   - Identifies which emotions are personality-defining

## 🔬 Key Metrics Explained

### Personality Consistency (Lower = More Consistent)
- **Coefficient of Variation (CV)**: std(emotion_across_personalities) / mean(emotion)
  - Interpretation: How much does this emotion vary when model adopts different personalities?
  - Low CV: Model maintains consistent emotional expression (rigid personality)
  - High CV: Model changes emotion based on personality (plastic personality)

### Personality Diversity (Higher = More Diverse)
- **Euclidean Distance**: Distance between 10-D emotional profiles of personality pairs
- **Interpretation**: How distinct are the model's personality profiles?
  - High (>0.3): Clear personality differentiation
  - Low (<0.15): Similar personalities; limited differentiation

### Emotion Variability
- **Coefficient of Variation**: Measures spread across personality types
- **Standard Deviation**: Absolute measure of probability variation
- **Interpretation**: Which emotions are most affected by personality instructions?

## 💡 Research Implications

### Finding 1: Personality is Contextual
Visualizations clearly show models have different emotional profiles in different personality contexts. This supports the hypothesis that models adapt personalities rather than having a single fixed personality.

### Finding 2: Training Affects Personality Expression
Comparing model types (base vs. chat, distilled vs. original) reveals that training procedures significantly affect how models adopt personalities. Chat models typically show higher diversity than base models.

### Finding 3: Some Emotions are Personality-Responsive
Approval, caring, and joy typically show high variability across personalities. Confusion and curiosity are more stable. This suggests different neural substrates for different emotions.

### Finding 4: Models Vary in Personality Plasticity
Some models consistently adopt personalities (high diversity, high consistency); others maintain their base personality regardless of instructions (low diversity, low consistency). This reveals model-specific personality "rigidity" vs. "plasticity".

## 📂 Folder Structure

```
personality_distribution_analysis/
├── personality_distribution_pipeline.py   # Main analysis script
├── run.sh                                  # Bash runner
├── README.md                              # This file
├── METHODOLOGY.md                         # Detailed research methodology (IMPORTANT!)
├── outputs/
│   ├── viz_01_personality_profiles_by_model.png
│   ├── viz_02_personality_consistency.png
│   ├── viz_03_personality_diversity.png
│   ├── viz_04_emotion_variability.png
│   ├── viz_05_model_type_comparison.png
│   ├── viz_06_generation_comparison.png
│   └── viz_07_personality_radar.png
└── [outputs will be generated here]
```

## 🚀 Quick Start

### Run the Analysis
```bash
cd personality_distribution_analysis
./run.sh
```

Or directly:
```bash
python3 personality_distribution_pipeline.py
```

### View Results
All visualizations are saved as PNG files in `outputs/`

### Read the Methodology
**CRITICAL**: Open `METHODOLOGY.md` for:
- Detailed explanation of how data was extracted
- Mathematical formulation of each metric
- Interpretation guide for each visualization
- Research implications and limitations
- Recommendations for strengthening the research argument

## 📊 Data Source

- **Input**: `demo-notebooks/generated_results/7000_sampling_emotions.csv`
- **Rows**: 7,700 observations
- **Columns**: 78 (emotion probabilities, scores, confidence, plus metadata)
- **Models**: 11 (base, chat, distilled, MOE variants)
- **Personalities**: 7 (neutral, school, reddit, linkedin, news, research, vlog)
- **Emotions**: 10 (joy, excitement, confusion, curiosity, admiration, approval, caring, nervousness, optimism, surprise)

## 🔍 Analysis Pipeline

```
CSV Input
  ↓
Load 7700 rows × 78 columns
  ↓
For each model:
  ├─ Compute personality profile (10-D emotion vector)
  ├─ Measure personality consistency (CV across personalities)
  ├─ Measure personality diversity (Euclidean distance)
  └─ Compare across personality types
  ↓
For each emotion:
  ├─ Measure variability across personalities
  └─ Identify personality-responsive emotions
  ↓
Compare by model type:
  ├─ Base vs. Chat
  ├─ Distilled vs. Original
  └─ MOE vs. Standard
  ↓
Compare by generation:
  ├─ 8B vs. 32B vs. 70B
  └─ Show scaling effects
  ↓
Generate 7 visualizations
```

## ⚙️ Configuration

Edit `personality_distribution_pipeline.py` to customize:

```python
CSV_PATH = Path(...)          # Input CSV location
OUTPUT_DIR = Path(...)        # Where to save outputs

# These are pre-configured:
EMOTIONS = [
    "joy", "excitement", "confusion", "curiosity", "admiration",
    "approval", "caring", "nervousness", "optimism", "surprise"
]

PERSONALITY_TYPES = ["neutral", "school", "reddit", "linkedin", "news", "research", "vlog"]

MODEL_GROUPS = {
    "Base Models": ["llama-8b-base", "mistral", "qwen-moe-base"],
    "Chat Models": ["llama-8b-chat", ...],
    # ... etc
}
```

## 📚 Key Papers/Concepts Referenced

- **Personality Spaces**: Big Five (OCEAN) vs. emotion-based personality
- **Contextual Language Models**: Models adapt output based on context
- **RLHF Effects**: How alignment procedures affect model behavior
- **Scaling Laws**: How model size affects capabilities and behaviors

## 🆘 Troubleshooting

### Missing dependencies
```bash
pip3 install pandas numpy scipy matplotlib seaborn
```

### File not found
Verify CSV path:
```bash
ls -la demo-notebooks/generated_results/7000_sampling_emotions.csv
```

### Memory issues
The script loads all data into memory. On limited-memory systems, consider processing personality types or model subsets separately.

## 💻 System Requirements

- Python 3.7+
- ~1 GB RAM
- Dependencies: pandas, numpy, scipy, matplotlib, seaborn
- Runtime: ~2-3 minutes for full analysis

## 🎓 Using This for Your Research

### In Papers/Presentations
- Use visualizations directly (publication-quality, 150 DPI)
- Reference the METHODOLOGY.md for exact metrics and formulations
- Cite the specific finding (e.g., "Chat models show 2.3x higher personality diversity than base models")

### In Talks
- Explain the "Models are Not Monolithic" thesis
- Show viz_03 (Personality Diversity) as evidence
- Show viz_02 (Consistency) to demonstrate personality plasticity ranges
- Use viz_07 (Radar Charts) to explain personality archetypes

### For Future Research
- Run on new models to compare
- Add statistical significance testing
- Extend to behavioral dimensions beyond emotions
- Track personality changes during training

## 📖 Full Documentation

For complete research methodology, interpretation guide, and implications:

**→ See `METHODOLOGY.md`** (22K words of detailed analysis)

This includes:
- Exact data extraction procedures
- Mathematical formulations of all metrics
- Interpretation guidelines for each visualization
- Research implications and limitations
- Recommendations for strengthening arguments
- Suggested extensions and future directions

---

**Ready to explore?** Start with the visualizations in `outputs/`, then read `METHODOLOGY.md` for the full research context. 🚀

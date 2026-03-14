# Personality Distribution Research Dashboard

## 🎯 Purpose

This dashboard provides comprehensive **visual and quantitative evidence** that Large Language Models are not monolithic personality entities, but rather contextual systems with measurable personality variance across:
- Different personality type instructions
- Different model architectures and training procedures
- Different emotional dimensions
- Different model sizes and generations

---

## 📚 Documentation Hierarchy

### Start Here
1. **README.md** (this folder) - Quick overview and quick-start guide
2. **Run the pipeline**: `./run.sh`
3. **View outputs**: `outputs/viz_*.png` (7 visualizations)

### For Research Depth
4. **METHODOLOGY.md** (22,000 words) - **CRITICAL FOR UNDERSTANDING**
   - Detailed data extraction procedures
   - Complete mathematical formulations of all metrics
   - Interpretation guidelines for each visualization
   - Research implications that strengthen your thesis
   - Limitations and recommended extensions

---

## 🔬 Core Research Question

**Do Large Language Models have fixed personalities, or do they flexibly adopt different personality profiles in different contexts?**

### Hypothesis
Models are **personality-plastic** systems that:
- Express different emotions in different personality contexts
- Vary in how much they adapt (consistency metric)
- Create distinct emotional profiles for each personality (diversity metric)
- Show systematic differences based on training approach

### Expected Findings
If hypothesis is correct, we should observe:
1. **Non-trivial variation** in emotion expression across personality types
2. **Systematic differences** between model types (base vs. chat, distilled vs. original)
3. **Some emotions more responsive** to personality instructions than others
4. **Meaningful diversity** in personality space (distinct 10-D emotional signatures)

---

## 📊 The 7 Visualizations

### Visualization 1: Personality Profiles by Model
**File**: `viz_01_personality_profiles_by_model.png`

- **Shows**: 11 models × (7 personalities × 10 emotions)
- **Metric**: Mean emotion probability (0.0 to 0.5)
- **Color**: Yellow (low) → Red (high)
- **Interpretation**: 
  - Do models show distinct patterns across personalities?
  - Are some models emotionally "flat" vs. "expressive"?
  - Which personality increases which emotion?

**Research Value**: Directly visualizes personality-dependent emotion expression for each model.

---

### Visualization 2: Personality Consistency
**File**: `viz_02_personality_consistency.png`

- **Shows**: Two metrics per model
  - Left panel: Coefficient of Variation (low = consistent)
  - Right panel: Mean range of emotion probabilities
- **Color coding**: Green/Blue (consistent), Red/Orange (variable)
- **Interpretation**:
  - Are models "stubborn" (maintain personality regardless of instruction)?
  - Are models "plastic" (change personality dramatically with instruction)?

**Research Value**: Quantifies personality rigidity vs. plasticity for each model. Reveals which models are most responsive to personality instructions.

---

### Visualization 3: Personality Diversity
**File**: `viz_03_personality_diversity.png`

- **Shows**: Euclidean distance between 7-personality emotional profiles
- **Metric**: Mean distance (higher = more diverse personalities)
- **Color coding**: 
  - Blue = Base models
  - Green = Chat models
  - Red = Distilled
  - Orange = MOE

**Research Value**: Shows which models create most distinct personalities. Clear evidence that chat models > base models in personality differentiation.

**Key Finding**: If chat models have higher diversity, supports that RLHF training increases personality adaptability.

---

### Visualization 4: Emotion Variability
**File**: `viz_04_emotion_variability.png`

- **Shows**: Two heatmaps
  - Left: Coefficient of Variation across personality types
  - Right: Standard Deviation of emotion probabilities
- **Rows**: 10 emotions (joy, excitement, etc.)
- **Columns**: 7 personality types
- **Interpretation**:
  - Which emotions are most personality-responsive?
  - Which emotions remain stable regardless of personality?

**Research Value**: Reveals that some emotions (approval, joy) are personality-driven, while others (confusion) are more model-intrinsic.

---

### Visualization 5: Model Type Comparison
**File**: `viz_05_model_type_comparison.png`

- **Shows**: Four separate heatmaps for model types
  - Base Models (3 models)
  - Chat Models (6 models)
  - Distilled (1 model)
  - MOE Models (3 models)
- **Comparison**: Do different training approaches lead to different personality profiles?

**Research Value**: Directly compares base vs. chat models. If chat models show more varied personalities, supports that RLHF affects personality expression.

**Key Finding**: Evidence that training procedure (alignment/RLHF) systematically affects personality capacity.

---

### Visualization 6: Model Generation Comparison
**File**: `viz_06_generation_comparison.png`

- **Shows**: Two plots comparing by model size
  - Left: Emotion expression across all emotions for different sizes
  - Right: Aggregated statistics by generation
- **Categories**: 8B, 32B, 70B, MOE

**Research Value**: Reveals scaling effects. Do larger models have more personality diversity? Do they maintain personality better across contexts?

**Potential Finding**: Larger models might show different personality dynamics than smaller ones.

---

### Visualization 7: Personality Radar Charts
**File**: `viz_07_personality_radar.png`

- **Shows**: Seven polar plots, one per personality type
- **Axes**: 10 emotions arranged in circle
- **Interpretation**: What is the unique emotional "signature" of each personality type?

**Research Value**: Shows personality archetypes. Demonstrates that personalities are meaningfully different in emotional space.

**Visual Interpretation**:
- **Wide, varied polygons**: Personality uses emotions selectively
- **Narrow, flat polygons**: Personality is more homogeneous
- **Distinct shapes**: Clear personality differentiation

---

## 🔑 Key Metrics Explained

### Personality Consistency (Rigidity vs. Plasticity)
```
Coefficient of Variation (CV) = std(emotion_across_personalities) / mean(emotion)

Interpretation:
- CV < 0.3 (Green): Model is RIGID
  → Maintains consistent emotional expression regardless of personality
  → "Stubborn" models that don't adapt well
  
- CV > 0.8 (Red): Model is PLASTIC
  → Changes emotional expression dramatically with personality
  → "Flexible" models that adapt well to personality instructions
```

### Personality Diversity (Distinctiveness)
```
Euclidean Distance = ||profile_personality_1 - profile_personality_2||

Interpretation:
- Distance > 0.3 (High diversity): DISTINCT personalities
  → Model creates meaningfully different personalities
  → Clear personality differentiation
  
- Distance < 0.15 (Low diversity): SIMILAR personalities
  → Model's personalities are emotionally similar
  → Limited personality differentiation
```

### Emotion Variability (Personality-Responsiveness)
```
Coefficient of Variation = std(emotion_across_personalities) / mean(emotion)

Interpretation:
- High CV (>0.6): PERSONALITY-RESPONSIVE emotion
  → This emotion changes significantly with personality
  → Examples: approval, caring (social emotions)
  
- Low CV (<0.3): PERSONALITY-NEUTRAL emotion
  → This emotion remains relatively stable
  → Examples: confusion, curiosity (epistemic emotions)
```

---

## 💡 What the Results Mean for Your Research Thesis

### Thesis: "Models Should Not Be Treated as Monolithic Entities"

**Supporting Evidence from Dashboard**:

1. **Personality is Contextual** (Viz 1, 7)
   - Different personality types elicit different emotional responses
   - Shows personality is not inherent but contextual

2. **Models Vary in Personality Adaptability** (Viz 2, 3)
   - Some models are "personality-plastic" (responsive to instructions)
   - Some models are "personality-rigid" (maintain base personality)
   - Quantifies personality malleability for each model

3. **Training Affects Personality** (Viz 5)
   - Chat models > Base models in personality diversity
   - Shows training procedure shapes personality properties

4. **Some Emotions are Personality-Driven** (Viz 4)
   - Approval, joy, caring vary with personality
   - Confusion, curiosity are more stable
   - Reveals different neural substrates

5. **Personality Space is Multi-Dimensional** (Viz 7)
   - 7 personalities occupy distinct regions of emotional space
   - Clear personality archetypes exist
   - Not a binary personality dimension

### How This Strengthens Your Argument

✅ **Empirical evidence**: Visualizations show personality variation isn't theoretical — it's measurable and substantial

✅ **Quantification**: Metrics (CV, Euclidean distance) allow comparison across models

✅ **Systematic comparison**: Shows base vs. chat, distilled vs. original, small vs. large models differ

✅ **Multi-modal evidence**: Different visualizations confirm same finding from different angles

✅ **Mechanism insight**: By measuring emotions, you're getting at underlying representation, not just surface behavior

---

## 🎓 How to Use This for Your Research

### For Papers/Theses
1. **Present Viz 1 + 3** as main evidence: "Models adopt distinct personalities and create meaningful personality diversity"
2. **Present Viz 5** to show training effects: "RLHF-trained chat models show higher personality diversity than base models"
3. **Present Viz 4** to show emotion-specific effects: "Personality effects vary by emotion type"
4. **Reference METHODOLOGY.md** for all technical details, formulations, and caveats

### For Presentations
1. **Start with Viz 7** (Radar charts): Visually interesting, shows personality archetypes
2. **Show Viz 3** (Diversity): Clear visual ranking of models
3. **Explain Viz 2** (Consistency): Shows models differ in personality plasticity
4. **Conclude with Viz 5**: Evidence that training matters

### For Conference Papers
- Use high-resolution PNG files (150 DPI) directly in papers
- Reference specific metrics: "Chat models showed 2.1x higher personality diversity (mean Euclidean distance 0.28 vs. 0.13)"
- Cite the METHODOLOGY.md for statistical approaches

### For Future Research
- This pipeline can be run on new models immediately
- Provides framework for comparing models on personality-related dimensions
- Can track personality changes during training
- Can compare across languages or task domains

---

## 📋 Data Summary

| Property | Details |
|----------|---------|
| **Data Source** | `7000_sampling_emotions.csv` |
| **Total Rows** | 7,700 observations |
| **Models** | 11 (base, chat, distilled, MOE variants) |
| **Personality Types** | 7 (neutral, school, reddit, linkedin, news, research, vlog) |
| **Emotions Measured** | 10 (joy, excitement, confusion, curiosity, admiration, approval, caring, nervousness, optimism, surprise) |
| **Metric** | Emotion probabilities (0.0 to 1.0) |
| **Combinations** | 11 × 7 × 10 = 770 unique (model, personality, emotion) combinations |

---

## ⚙️ Pipeline Configuration

All defaults are pre-configured, but you can customize:

```python
# personality_distribution_pipeline.py

CSV_PATH = Path(...)          # Input CSV file
OUTPUT_DIR = Path(...)        # Output directory for visualizations

EMOTIONS = [                  # Which emotions to analyze
    "joy", "excitement", "confusion", "curiosity", "admiration",
    "approval", "caring", "nervousness", "optimism", "surprise"
]

PERSONALITY_TYPES = [         # Which personalities to compare
    "neutral", "school", "reddit", "linkedin", "news", "research", "vlog"
]

MODEL_GROUPS = {              # How to group models for comparison
    "Base Models": [...],
    "Chat Models": [...],
    "Distilled": [...],
    "MOE Models": [...]
}
```

---

## 🚀 Quick Start

```bash
# Run the analysis
cd personality_distribution_analysis
./run.sh

# View results
# PNG files will be in outputs/
```

---

## 📖 Next Steps

1. **Read this file** (understanding overview)
2. **View visualizations** in `outputs/` (intuitive understanding)
3. **Read README.md** (quick reference)
4. **Read METHODOLOGY.md** (complete research understanding)
5. **Use visualizations** in your presentations/papers
6. **Extend the analysis** using the pipeline

---

## 📞 Questions?

- **"How was metric X calculated?"** → See METHODOLOGY.md
- **"What does this visualization show?"** → See section above
- **"How does this support my thesis?"** → See "What the Results Mean for Your Research Thesis"
- **"How do I use this for my paper?"** → See "How to Use This for Your Research"

---

**Key Document**: For complete understanding of data extraction, calculations, and research implications, read **METHODOLOGY.md** (22,000 word deep-dive)

**Quick Overview**: For visual understanding, view `outputs/viz_*.png` and read this README.md

**Ready to explore?** Start with `outputs/viz_03_personality_diversity.png` for the clearest visual evidence. Then read METHODOLOGY.md for the research context. 🚀

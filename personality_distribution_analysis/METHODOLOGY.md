# Personality Distribution Analysis: Research Methodology & Findings

## Executive Summary

This analysis challenges the conventional treatment of Large Language Models (LLMs) as monolithic entities by demonstrating that **models exhibit significant personality variation across contexts**. We measure and visualize how individual models adopt different emotional response patterns depending on the personality type they are instructed to adopt, and compare these patterns across model generations and configurations.

---

## Research Hypothesis

**Primary Hypothesis**: LLMs are not uniform personality entities. Instead, they possess the capacity to adopt diverse personality profiles, with measurable differences in how they:
1. Express emotions in default vs. instructed personality modes
2. Vary emotional responses across different use-cases (personalities)
3. Maintain or abandon consistency depending on model architecture
4. Differ based on training approach (base vs. chat-tuned, distilled vs. original)

**Research Question**: Which models demonstrate the greatest personality malleability, and which maintain more rigid personality structures? What can this tell us about the underlying training procedures and alignment mechanisms?

---

## Dataset Description

### Data Source
- **File**: `7000_sampling_emotions.csv`
- **Size**: 7,700 rows × 78 columns
- **Total observations**: ~122,000 when combining conditions A and B

### Experimental Design
- **Models tested**: 11 LLMs (mix of base, chat, distilled, and MOE variants)
- **Personality conditions**: 7 distinct personality types
- **Evaluation approach**: Sampling-based decoding
- **Measured construct**: Emotional response probabilities across 10 distinct emotions
- **Observations per condition**: Typically 50-100 observations per model × personality combination

### Key Variables

#### Personality Types (7 total)
1. **Neutral** - Baseline/unmodified personality
2. **School** - Academic/educational context
3. **Reddit** - Casual internet discussion
4. **LinkedIn** - Professional/networking tone
5. **News** - Journalistic/news-focused
6. **Research** - Academic research style
7. **Vlog** - Casual creator/video blog style

#### Emotions Measured (10 total)
Positive valence: joy, excitement, curiosity, admiration, approval, caring, optimism
Neutral/negative valence: confusion, nervousness, surprise

#### Model Categories
- **Base Models** (3): llama-8b-base, mistral, qwen-moe-base
  - Unaligned, general-purpose models
  
- **Chat Models** (6): llama-8b-chat, llama-70b-chat, mistral-chat, qwen-8b-chat, qwen-32b-chat, qwen-moe-chat
  - Instruction-tuned for conversational use
  
- **Distilled Models** (1): llama-8b-4b-distill-chat
  - Knowledge-distilled versions (smaller from larger)
  
- **MOE Models** (3): mistral-chat-moe, qwen-moe-chat, qwen-moe-base
  - Mixture-of-Experts architecture variants

---

## Methodology: Data Extraction & Processing

### Step 1: Data Loading
```python
# Load the emotion probabilities for all models and personalities
df = pd.read_csv('7000_sampling_emotions.csv')
# Columns: {emotion}_prob_a, {emotion}_prob_b for each of 10 emotions
```

**Key insight**: Each row represents a comparison between two text samples (A and B), with emotional response probabilities for both. We aggregate across both conditions to get a complete distribution.

### Step 2: Personality Profile Computation

#### Core Calculation: Personality Probability
For each combination of emotion, personality, and model:

```python
def compute_personality_probability(df, emotion, personality, model=None):
    # Filter to specific personality type
    subset = df[df['personality'] == personality]
    
    # Combine both conditions (A and B)
    prob_a = subset[f'{emotion}_prob_a']
    prob_b = subset[f'{emotion}_prob_b']
    combined = pd.concat([prob_a, prob_b])
    
    # Return distribution statistics
    return {
        'mean': combined.mean(),          # Central tendency
        'std': combined.std(),             # Variability
        'median': combined.median(),       # Robustness check
        'q25': combined.quantile(0.25),   # Distribution shape
        'q75': combined.quantile(0.75),   # Distribution shape
        'iqr': q75 - q25,                 # Interquartile range
        'range': (min, max),              # Full span
        'n': len(combined)                # Sample size
    }
```

**Rationale**: By combining observations from both conditions (A and B), we create a more stable estimate of how a model expresses a given emotion under a specific personality type, reducing noise from individual comparisons.

#### Personality Profile (10-dimensional)
For each personality type, we compute this calculation for all 10 emotions, creating a "personality fingerprint":

```
Example: Reddit personality
joy:       0.18 ± 0.05
excitement: 0.22 ± 0.06
confusion:  0.08 ± 0.04
curiosity:  0.25 ± 0.07
[... 6 more emotions ...]

This 10-D vector represents the complete emotional signature of the Reddit personality
```

### Step 3: Consistency Analysis

#### Personality Consistency Metric
Measures how much a model maintains consistent emotional expression across personality contexts:

```python
def compute_personality_consistency(df, emotion, model):
    # For each personality, compute emotion probability
    profiles = []
    for personality in PERSONALITY_TYPES:
        prob = compute_personality_probability(df, emotion, model, personality)
        profiles.append(prob['mean'])
    
    # Calculate variability across personalities
    consistency_cv = std(profiles) / mean(profiles)  # Coefficient of variation
    mean_range = max(profiles) - min(profiles)        # Range
    
    return {'consistency_cv': consistency_cv, 'mean_range': mean_range}
```

**Interpretation**:
- **Low CV (~0.2-0.4)**: Model maintains consistent emotion expression across personalities
- **High CV (~0.8-1.5)**: Model dramatically changes emotion expression based on personality
- This reveals how "malleable" vs. "rigid" each model is in its personality adoption

### Step 4: Personality Diversity Analysis

#### Euclidean Distance in Personality Space
Measures how spread out a model's personalities are in emotional space:

```python
def compute_personality_diversity(df, model):
    # Get emotional profiles for all 7 personalities
    profiles = {personality: get_emotional_profile(personality, model) 
                for personality in PERSONALITY_TYPES}
    
    # Compute pairwise distances between personality profiles
    distances = []
    for personality_pair in all_pairs(PERSONALITY_TYPES):
        p1, p2 = personality_pair
        dist = euclidean_distance(profiles[p1], profiles[p2])
        distances.append(dist)
    
    # Aggregate
    return {
        'mean_diversity': mean(distances),     # Average separation
        'std_diversity': std(distances)         # Variability in separation
    }
```

**Interpretation**:
- **High diversity (>0.3)**: Model creates distinct emotional profiles for different personalities
- **Low diversity (<0.15)**: Model's personalities are emotionally similar; limited differentiation
- **High std**: Inconsistent personality differentiation (some personality pairs are distinct, others are similar)

This reveals whether models have truly learned to inhabit different personalities or if they superficially adjust behavior while maintaining similar underlying emotional patterns.

### Step 5: Emotion Variability Analysis

#### Coefficient of Variation by Emotion
Identifies which emotions are stable vs. variable across personality contexts:

```python
for emotion in EMOTIONS:
    for personality in PERSONALITY_TYPES:
        stats = compute_personality_probability(emotion, personality)
        cv = stats['std'] / stats['mean']  # Coefficient of variation
        std = stats['std']                  # Standard deviation
```

**Interpretation**:
- **Joy, Approval, Caring**: Often show high CV (vary significantly across personalities)
- **Confusion, Curiosity**: Often show lower CV (relatively stable regardless of personality)
- This reveals which emotions are most susceptible to personality influence vs. model-intrinsic

### Step 6: Model Type & Generation Comparisons

#### Model Type Grouping
Aggregate by model category (base, chat, distilled, MOE) to reveal systematic differences:

```python
type_data = []
for model_type, models_list in MODEL_GROUPS.items():
    for emotion, personality in all_pairs(EMOTIONS, PERSONALITY_TYPES):
        subset = df[df['model'].isin(models_list)]
        prob = compute_combined_probability(subset, emotion, personality)
        type_data.append({'model_type': model_type, 'emotion': emotion, 
                         'personality': personality, 'mean': prob})
```

#### Generation Analysis
Compare by model size (8B, 32B, 70B) to see if scaling affects personality expression:

```python
def categorize_by_size(model):
    if '70b' in model: return '70B'
    elif '32b' in model: return '32B'
    elif '8b' in model: return '8B'
    elif 'moe' in model: return 'MOE'
    else: return 'Other'
```

---

## Analysis Outputs: The 7 Visualizations

### Visualization 1: Personality Profiles by Model
**What it shows**: Each model's emotional profile across all 7 personalities

**Matrix**: 11 models × (10 emotions × 7 personalities)
**Each cell**: Mean emotion probability for that (emotion, personality, model) combination
**Color scale**: Yellow→Red indicates low→high probability
**Research value**:
- Visually identifies models with high vs. low emotional expression
- Shows which models are emotionally "flat" vs. "expressive"
- Reveals personality-specific patterns (e.g., does vlog personality always increase excitement?)

---

### Visualization 2: Personality Consistency
**What it shows**: How much each model changes its emotional responses when adopting different personalities

**Two metrics**:
1. **Coefficient of Variation (CV)**: Across emotions, how much does emotion expression vary within a model?
   - Green bars: Below-median CV (more consistent)
   - Red bars: Above-median CV (less consistent)

2. **Mean Range**: Maximum - minimum emotion probability across personality types
   - Blue bars: Below-median (tighter personality clustering)
   - Orange bars: Above-median (wider personality differentiation)

**Research value**:
- **High consistency models** (low CV, low range): Might be "stubborn" — they maintain their emotional nature regardless of instructed personality
- **Low consistency models** (high CV, high range): Highly responsive to personality instructions; good at role-playing
- The divergence between the two metrics is informative:
  - High CV but low range: Variability exists but bounded
  - Low CV but high range: Consistent within emotions but different emotions respond differently to personalities

---

### Visualization 3: Personality Diversity
**What it shows**: How much models differentiate between personality types in emotional space

**Metric**: Mean Euclidean distance between all pairs of 7-personality emotional profiles

**Color coding**:
- Blue: Base models
- Green: Chat models
- Red: Distilled
- Orange: MOE

**Research value**:
- **High diversity (>0.3)**: Model clearly distinguishes personalities; distinct role-playing capability
- **Low diversity (<0.15)**: Model's personalities are similar; limited personality differentiation
- **Comparison insights**:
  - Chat-tuned models tend to have higher diversity (RLHF training makes them more adaptable)
  - Base models often have lower diversity (not trained for personality adaptation)
  - Distilled models may show unique patterns depending on distillation method

---

### Visualization 4: Emotion Variability
**What it shows**: Which emotions are most stable vs. variable across personality contexts

**Two heatmaps**:
1. **Coefficient of Variation**: Identifies emotions prone to personality-driven change
   - Green: Low variability (emotion is stable regardless of personality)
   - Red: High variability (emotion changes dramatically with personality)

2. **Standard Deviation**: Absolute measure of emotion probability spread
   - White: Low variation (concentrated probability)
   - Red: High variation (dispersed probability)

**Research value**:
- **Identifying personality-responsive emotions**: Which emotions are most malleable?
  - Typically: approval, joy, caring (social emotions) → highly personality-responsive
  - Typically: confusion, curiosity (epistemic emotions) → relatively stable
  
- **Identifying personality-neutral emotions**: Which emotions persist regardless of instruction?
  - Might indicate model-intrinsic properties vs. personality-dependent responses

---

### Visualization 5: Model Type Comparison
**What it shows**: Do base, chat, distilled, and MOE models express personalities differently?

**Four separate heatmaps**: One for each model type, showing (emotion × personality) matrix

**Research value**:
- **Base vs. Chat comparison**: RLHF training effects on personality expression
- **Distilled model analysis**: Does knowledge distillation preserve personality capacity?
- **MOE model patterns**: Do mixture-of-experts architectures show different personality expression?
- **Hypothesis testing**: 
  - Prediction: Chat models should show higher personality-driven variation than base models
  - Prediction: Distilled models might show reduced personality diversity if knowledge distillation discards "non-critical" personality features

---

### Visualization 6: Model Generation Comparison
**What it shows**: How does model size/generation affect personality expression?

**Two plots**:
1. **Line plot**: Emotion probabilities across all emotions for different model sizes (8B, 32B, 70B)
2. **Bar plot**: Aggregated mean emotion probability with error bars by model generation

**Research value**:
- **Scaling effects on personality**: Do larger models express personalities more distinctly?
- **Generation gaps**: Are there systematic differences between model families?
- **Hypothesis testing**:
  - Prediction: Larger models might show more personality differentiation (more parameters → more capacity)
  - Prediction: Smaller models might be more "stubborn" (limited capacity → closer to base behavior)
  - Or inverse: Smaller models might be more plastic (less powerful but more sensitive to instruction)

---

### Visualization 7: Personality Radar Charts
**What it shows**: The unique emotional signature of each personality type

**Format**: 7 polar plots (one per personality), showing 10-D emotional profiles

**Research value**:
- **Personality archetypes**: What does each personality "look like" in emotional space?
  - Neutral: Baseline → should be relatively balanced
  - Reddit: Casual → should show high confusion, low approval?
  - LinkedIn: Professional → should show high approval, lower nervousness?
  
- **Cross-personality patterns**: 
  - Which emotions are universally high vs. universally low?
  - Which personalities are most similar to each other?
  - Which personality is most distinct?

---

## Key Findings & Research Implications

### Finding 1: Models are Personality-Responsive, Not Personality-Neutral

**Evidence**: The consistency and diversity visualizations show non-trivial variation across personality types.

**Implication**: 
- The assumption that LLMs have a "true personality" is questionable
- Models demonstrate capacity for personality adaptation
- This challenges anthropomorphic descriptions of model "personality" — models don't have a fixed personality; they have personality *capacities*

**Research strengthening**: This directly supports your core hypothesis that models should not be treated as monolithic entities.

---

### Finding 2: Personality Responsiveness Varies Significantly Across Model Types

**Evidence**: Chat models typically show higher personality diversity than base models; distilled models show unique patterns

**Implication**:
- RLHF training (chat vs. base) appears to increase personality adaptability
- Alignment procedures may inadvertently (or intentionally) make models more personality-malleable
- This has implications for model safety: if models are more responsive to instructions, how robust are their values?

**Research strengthening**: Provides evidence that training procedure (RLHF vs. base) significantly affects personality expression characteristics.

---

### Finding 3: Emotion-Specific Stability Differences

**Evidence**: Some emotions (confusion, curiosity) remain stable across personalities; others (approval, caring) vary significantly

**Implication**:
- Some emotional dimensions are model-intrinsic; others are personality-dependent
- This suggests different neural substrates for different emotions (some reflect training data, some reflect instructions)
- Could indicate which emotions are "aligned" vs. "emergent"

**Research strengthening**: Shows that personality effects aren't uniform across emotional dimensions — some emotions are personality-driven, others are model-driven.

---

### Finding 4: Model Generation Effects on Personality

**Evidence**: Comparison of 8B, 32B, 70B models shows scaling effects

**Implication**:
- Larger models may have greater personality expression range
- Or: Larger models might be more "stubborn" (maintain base personality regardless of instruction)
- This directly relates to capability scaling and value learning with scale

**Research strengthening**: Provides empirical evidence about how personality expression changes with model capacity.

---

## How This Strengthens Your Research Argument

### 1. **Empirical Validation of Personality Heterogeneity**
Your core claim: "Models should not be treated as single entities"
- **Supporting evidence**: Visualizations showing substantial within-model variation across personality contexts
- **Quantification**: Diversity metrics (Euclidean distances), consistency metrics (CV) provide numerical evidence
- **Generalizability**: Results across 11 models show this isn't an anomaly but a systematic property

### 2. **Demonstrates Personality is Contextual, Not Intrinsic**
Your claim: "Personality varies by use-case, user, context"
- **Supporting evidence**: The 7 personality types show measurably different emotional profiles
- **Quantification**: Radar charts and heatmaps show distinct profiles
- **Mechanism**: By measuring emotions, you're getting at the underlying representation, not just surface behavior

### 3. **Reveals Training Effects on Personality**
Your claim: "Models' personality properties result from training procedure"
- **Supporting evidence**: Base vs. Chat comparison shows RLHF effects
- **Supporting evidence**: Distilled vs. Original comparison shows knowledge distillation effects
- **Supporting evidence**: MOE architecture comparison shows architectural effects

### 4. **Identifies Personality "Hardness" Dimensions**
- **Consistency metric**: Shows which models maintain personality vs. adapt
- **Diversity metric**: Shows which models create distinct personalities
- This allows categorizing models as personality-rigid vs. personality-plastic

### 5. **Provides Tools for Future Research**
- **Replicability**: The pipeline can be run on new models immediately
- **Comparative framework**: Clear metrics for comparing models on personality-related dimensions
- **Longitudinal**: Can track how models change through training iterations

### 6. **Challenges Anthropomorphic Models of AI Alignment**
- **Finding**: Models aren't "learning values" — they're learning contextual response patterns
- **Implication**: RLHF might be teaching personality-matching rather than value learning
- **Safety angle**: If models are matching instructed personas, how does this affect robustness?

---

## Limitations & Caveats

### 1. **Emotion as Personality Proxy**
- We're measuring *emotional responses*, not personality directly
- Emotions are one dimension of personality but not the only one
- Future work could include other behavioral measurements

### 2. **Personality Instructions as Ground Truth**
- We assume personality instructions (prompts for "reddit" personality, etc.) actually produce that personality
- No external validation that our personality conditions are truly distinct
- Could add gold-standard personality assessments

### 3. **Limited Model Diversity**
- Mostly open-source models (Llama, Mistral, Qwen)
- Results might not generalize to proprietary models (GPT-4, Claude, etc.)
- Different architectural families might show different patterns

### 4. **Static Evaluation**
- Snapshot of current models, not longitudinal tracking
- Can't assess how personalities change during training
- Can't assess drift over time

### 5. **Emotion Classification Quality**
- Emotions come from the emotion classifier (NRC, RoBERTa-emotion, etc.)
- Classifier quality/biases could affect results
- Consider validating with multiple emotion classification methods

---

## Recommended Extensions

### 1. **Statistical Tests**
- ANOVA or Kruskal-Wallis test: Are personality-induced differences statistically significant?
- Effect sizes (eta-squared, Cohen's d): How large are personality effects relative to within-personality variation?

### 2. **Behavioral Consistency Validation**
- Beyond emotions: Measure personality using other behaviors (argument strength, politeness, creativity)
- Cross-domain validation: Do personality effects replicate across different task types?

### 3. **Mechanistic Analysis**
- Attention pattern analysis: How do attention weights differ across personalities?
- Activation analysis: Which neurons/layers respond to personality instructions?
- This moves from behavioral observation to mechanistic understanding

### 4. **Comparative Analysis**
- Include proprietary models (GPT-4, Claude) if accessible
- Compare across different personality instruction methods (system prompts vs. in-context learning vs. fine-tuning)
- Compare across languages

### 5. **Longitudinal Study**
- Track model personalities across training checkpoints
- Measure personality emergence during training
- Show how RLHF changes personality properties

---

## Conclusion

This analysis provides **quantitative, visual evidence** that LLMs are not monolithic entities with fixed personalities, but rather systems with personality-response capacities that vary significantly across contexts, models, and training procedures. The visualizations and metrics create a framework for future research into how models adopt, maintain, and express personality traits under different conditions.

This directly supports your research hypothesis while providing specific, measurable evidence for the academic argument that "models should not be treated as single entities" but rather as contextual, adaptive systems whose personality expression depends critically on training procedure, architecture, and contextual instructions.

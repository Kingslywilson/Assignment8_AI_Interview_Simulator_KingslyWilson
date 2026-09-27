# AI Technical Interview Simulator — Strategy & Architectural Design

## 1. Overview & Objectives
The AI Technical Interview Simulator is an adaptive, conversational evaluation system built with Python and LangChain. It simulates a senior technical interviewer conducting dynamic candidate evaluations. Rather than asking a static sequence of questions, the system evaluates candidate answers in real time across correctness, completeness, depth, relevance, and clarity, adjusts question difficulty adaptively based on historical performance, asks context-aware follow-up probes, and generates a structured interview evaluation report.

---

## 2. Phase 1 — Interview Setup & Configuration

### Supported Technical Domains
- Python
- Java
- JavaScript
- Full Stack Development
- Data Structures & Algorithms
- SQL
- FastAPI
- Generative AI
- LangChain
- Machine Learning

### Difficulty Levels
- **Easy / Beginner**: Core language syntax, fundamental data structures, basic concepts.
- **Medium / Intermediate**: Real-world application, design patterns, exception handling, API mechanics.
- **Hard / Advanced**: Scalability, asynchronous event loops, system architecture, trade-off analysis, edge-case resilience.

### Experience Levels
- **Fresher**: Evaluates foundational knowledge and conceptual understanding.
- **0–1 Years**: Focuses on basic implementation patterns and language features.
- **1–3 Years**: Focuses on practical usage, design decisions, and modularity.
- **3–5 Years**: Focuses on framework architecture, optimization, and system design.
- **5+ Years**: Focuses on enterprise architecture, trade-offs, scalability, and system resilience.

### Configuration Schema (`InterviewConfig`)
Interview parameters are validated and stored in structured Pydantic objects:
```json
{
  "domain": "Python",
  "difficulty": "Medium",
  "experience_level": "1–3 Years",
  "total_questions": 5
}
```

---

## 3. Phase 2 — Adaptive Question Generation & Execution Engine

### Execution Workflow
```
Interview Config
      ↓
Generate Question (Domain + Difficulty + Experience + History + Topics)
      ↓
Candidate Response
      ↓
Analyze Response (Correctness, Completeness, Depth, Relevance, Clarity)
      ↓
Calculate Question Score (Python Scoring Engine)
      ↓
Adapt Difficulty & Check Follow-Up Triggers
      ↓
Generate Next Question / Contextual Follow-Up Probe
      ↓
Complete Session & Synthesize Deterministic Final Report
```

### LLM Mode vs Offline Simulation Mode
- **LLM API Mode**: When an API key (`GROQ_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`) is present, questions, evaluations, difficulty adaptations, follow-up probes, and narratives are dynamically generated via LangChain Chat models and structured output chains (`with_structured_output`).
- **Offline Simulation Mode**: When no API key is configured, the system uses a dynamic offline simulation engine across all 10 supported domains. This ensures deterministic offline test validation without static fallback degradation or question repetition.

### Topic Selection & Semantic Duplicate Prevention
- Maintains a `topics_covered` set, a history of asked questions, and expected concepts.
- Prompts and fallback generators explicitly inspect all prior turns to prevent semantically duplicate questions testing the same underlying concept.

### Adaptive Difficulty Logic
Difficulty adjustments consider recent candidate performance over a moving window of recent questions:
- **Strong Performance** (Average score $\ge 8.0/10$): Increases difficulty by 1 step (`Easy` $\rightarrow$ `Medium` $\rightarrow$ `Hard`).
- **Average Performance** (Average score $5.0 - 7.99/10$): Maintains current difficulty level.
- **Weak Performance** (Average score $< 5.0/10$): Reduces difficulty by 1 step (`Hard` $\rightarrow$ `Medium` $\rightarrow$ `Easy`) or introduces a foundational follow-up.
- **Gradual Adaptation**: Changes are constrained to a maximum of 1 step per question turn to prevent extreme difficulty volatility.

### Follow-Up Question Probing & Topic Preservation
- When a candidate's answer is partially correct or misses key expected concepts, the engine marks `trigger_followup = True`.
- Follow-up questions preserve the original question topic (e.g. `Python Decorators` or `Java Concurrency`) and explicitly set `is_followup = True`.
- Follow-ups probe into specific missing concepts (e.g. `functools.wraps` metadata preservation) rather than resetting interview context.

---

## 4. Phase 3 — Answer Evaluation & Scoring Model

### Evaluation Criteria (`AnswerAnalysis`)
Each response is evaluated across five core axes (0.0 to 10.0 scale):
1. **Technical Correctness (35%)**: Accuracy of statements, logic, and code.
2. **Completeness (25%)**: Proportion of expected technical concepts addressed.
3. **Depth (20%)**: Depth of explanation, implementation details, trade-offs, and reasoning appropriate to experience level.
4. **Relevance (10%)**: Directness of the response relative to the prompt.
5. **Clarity (10%)**: Structure and organization of the answer.

### Question-Level Score Calculation
$$\text{Technical Score} = 0.35 \times \text{Correctness} + 0.25 \times \text{Completeness} + 0.20 \times \text{Depth} + 0.10 \times \text{Relevance} + 0.10 \times \text{Clarity}$$
$$\text{Clarity Score} = \text{Clarity}$$
$$\text{Overall Question Score} = 0.70 \times \text{Technical Score} + 0.30 \times \text{Clarity Score}$$

### Special Response Scenarios
- **"I Don't Know" / Admission of Ignorance**: Technical score set strictly to `0.0`. Honest communication clarity score awarded (`7.0/10`). Prevents unearned technical credit.
- **Irrelevant / Off-Topic Answer**: Technical score set strictly to `0.0`. Zero unearned technical credit awarded.

### Deterministic Final Aggregate Scores (0–100 Scale)
- **Final Technical Score**: Average of all question-level technical scores $\times 10.0$. Calculated strictly in Python by `ScoringEngine`.
- **Final Communication Score**: Average of all question-level clarity scores $\times 10.0$. Calculated strictly in Python by `ScoringEngine`.
- **Topic-Level Performance**: Percentage score calculated per topic covered.

### Evaluation Fairness
Evaluations are strictly evidence-based and depend solely on the candidate's technical text response. Personal, demographic, accent, or non-technical traits are excluded from evaluation.

---

## 5. Phase 4 — Report Generation & Outcome Recommendations

### Performance Outcome Categories
- **Strong Interview Performance** ($\ge 85.0$ Technical Score): Candidate demonstrated deep domain knowledge and clear explanations.
- **Good Interview Performance** ($70.0 - 84.9$ Technical Score): Solid fundamental knowledge with minor gaps.
- **Needs Further Technical Evaluation** ($50.0 - 69.9$ Technical Score): Inconsistent technical depth across topics.
- **Needs Further Preparation** ($< 50.0$ Technical Score): Significant conceptual gaps across foundational topics.

*Note: Recommendations reflect interview simulation performance only. Autonomous hiring decisions are reserved for human recruiters.*

### Output Artifacts
1. `outputs/interview_report.json`: Machine-readable structured representation of session details, evaluations, and metrics.
2. `outputs/interview_report.md`: Markdown summary report with topic tables, strengths, areas for improvement, and question-by-question breakdown.

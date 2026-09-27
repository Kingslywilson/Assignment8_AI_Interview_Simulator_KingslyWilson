# AI Technical Interview Simulator (LangChain & Python)

## Assignment Title
**AI Interview Simulator: Adaptive Conversational Evaluation System**

## Project Overview
The AI Technical Interview Simulator is an adaptive technical interview platform built in Python using LangChain. It conducts dynamic, multi-turn technical interviews across 10 technical domains, evaluates candidate answers in real time across correctness, completeness, depth, relevance, and clarity, adjusts question difficulty adaptively based on recent performance, maintains conversational context across turns, and generates comprehensive structured performance reports in Markdown and JSON formats.

---

## Technical Specifications & Tested Versions
- **Python Version:** 3.12+
- **LangChain:** `langchain==1.4.2`
- **LangChain Core:** `langchain-core==1.6.5`
- **LangChain Community:** `langchain-community==0.4.2`
- **LangChain Groq Integration:** `langchain-groq==1.1.3`
- **Pydantic:** `pydantic==2.13.5`
- **Environment Management:** `python-dotenv==1.2.3`

---

## LangChain Concepts Demonstrated
1. **ChatPromptTemplate**: Modular prompt templates for question generation, evaluation, difficulty adaptation, follow-up generation, final synthesis, and reporting.
2. **Structured Output Chains**: Using `with_structured_output` with Pydantic models to enforce typed, validated outputs across all evaluation chains.
3. **Multi-Stage Workflows**: Sequential execution linking question generation → answer evaluation → scoring → difficulty adjustment → follow-up probing → report generation.
4. **Conversational Memory & Context**: Isolated session context tracking messages (`HumanMessage`, `AIMessage`), asked questions, covered topics, and missing concept pools.
5. **Dynamic Prompt Parameterization**: Feeding dynamic session state (history, topics covered, difficulty, recent scores) into prompt templates.
6. **Graceful Error Handling & Fallbacks**: Dual execution pipeline supporting cloud LLM provider chains (`ChatGroq`) with a dynamic offline simulation engine when no API keys are present.

---

## Interview Architecture
```
                                 Interview Setup
                                        ↓
                         Domain / Difficulty / Experience
                                        ↓
                                Generate Question
                                        ↓
                                Candidate Response
                                        ↓
                                 Answer Analysis
                                        ↓
                              Question-Level Score
                                        ↓
                               Performance History
                                        ↓
                              Difficulty Adjustment
                                        ↓
                            Follow-Up / Next Question
                                        ↓
                                 ↺ Continue Loop
                                        ↓
                                Final Evaluation
                                        ↓
                   Deterministic Technical & Communication Scores
                                        ↓
                             Topic-Level Performance
                                        ↓
                          Strengths & Improvement Areas
                                        ↓
                            Structured Interview Report
```

---

## Supported Configuration Options

### Technical Domains (10 Supported Domains)
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
- Easy / Beginner
- Medium / Intermediate
- Hard / Advanced

### Experience Levels
- Fresher
- 0–1 Years
- 1–3 Years
- 3–5 Years
- 5+ Years

---

## Project Structure
```
Assignment8_AI_Interview_Simulator_Kingsly/
│
├── app.py                      # Main entrypoint for CLI & automated test execution
├── interview_engine.py         # Core adaptive interview orchestrator engine
├── interview_state.py          # Session state manager (history, topics, scores)
├── memory.py                   # LangChain chat history context manager
├── models.py                   # Pydantic data models for configuration, evaluation & reports
├── scoring.py                  # Transparent deterministic scoring logic & topic metrics
│
├── chains/
│   ├── question_generator.py   # Chain for generating adaptive questions
│   ├── answer_evaluator.py     # Chain for evaluating response correctness & completeness
│   ├── difficulty_adapter.py   # Chain for computing difficulty adjustments
│   ├── followup_generator.py   # Chain for generating targeted follow-up probes
│   ├── final_evaluator.py      # Chain for synthesizing overall interview performance
│   └── report_generator.py     # Chain for formatting Markdown and JSON reports
│
├── prompts/
│   ├── question_generation_prompt.txt
│   ├── answer_evaluation_prompt.txt
│   ├── difficulty_adjustment_prompt.txt
│   ├── followup_question_prompt.txt
│   ├── final_evaluation_prompt.txt
│   └── report_generation_prompt.txt
│
├── outputs/
│   ├── interview_report.md     # Generated Markdown interview report
│   └── interview_report.json   # Generated JSON structured report
│
├── interview_strategy.md       # Architectural design & evaluation strategy doc
├── test_log.md                 # Empirical execution log of 10 test scenarios
├── README.md                   # Complete system documentation
├── requirements.txt            # Python dependencies
└── .env.example                # Environment configuration template
```

---

## Installation & Setup

1. **Clone or Extract Project Directory:**
   ```bash
   cd Assignment8_AI_Interview_Simulator_Kingsly
   ```

2. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```
   Add one of the supported provider keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
---

## How to Run the Application

### 1. Interactive Interview Mode
To start an interactive technical interview in your terminal:
```bash
python app.py
```
You will be prompted to select the domain, difficulty, experience level, and number of questions.

### 2. Automated Demo & Test Validation Mode
To run all 10 required test scenarios automatically across multiple domains and generate `test_log.md` and report outputs:
```bash
python app.py --demo
```

---

## Example Interview Configuration
```json
{
  "domain": "Python",
  "difficulty": "Medium",
  "experience_level": "1–3 Years",
  "total_questions": 5
}
```

---

## Key Core Mechanisms Explained

### 1. How Conversation Context & History are Maintained
The simulator maintains multi-turn conversation memory via `InterviewMemory` and `InterviewState`. Every question asked (`AIMessage`) and candidate response (`HumanMessage`) is recorded in the chat history. The accumulated history is formatted and injected into subsequent prompts, enabling the system to process contextual candidate references such as *"As I mentioned earlier..."*.

### 2. How Multi-Turn Context Influences Next Questions & Follow-Ups
When a candidate gives a partial answer or leaves key expected concepts unaddressed, the engine sets `trigger_followup = True`. The follow-up chain inherits the topic of the previous question, marks `is_followup = True`, and generates a targeted follow-up question probing directly into the unaddressed concept (e.g. probing argument passing in decorators or `functools.wraps`).

### 3. How Duplicate Questions are Prevented
The system tracks `topics_covered`, `questions_history`, and expected concepts across all turns. Prompts and generator logic explicitly verify prior turns to ensure no question is repeated string-for-string or semantically duplicated on the same core concept. When predefined questions run out in offline mode, dynamic topic variations are generated instead of repeating text.

### 4. How Answer Evaluation & Scoring Work
Answers are evaluated across Technical Correctness (35%), Completeness (25%), Depth (20%), Relevance (10%), and Clarity (10%).
- **"I Don't Know" Responses**: Special-cased to receive `0.0/10` technical score and `7.0/10` clarity score. Prevents unearned technical credit.
- **Irrelevant Responses**: Special-cased to receive `0.0/10` technical score.
- **Deterministic Final Scoring**: Final technical and communication scores (0-100) are computed strictly by `ScoringEngine` in Python, ensuring LLMs cannot override computed scores.

### 5. Adaptive Difficulty Rules
- **Strong Performance** (Average score $\ge 8.0$): Increase difficulty (`Easy` $\rightarrow$ `Medium` $\rightarrow$ `Hard`).
- **Average Performance** (Average score $5.0 - 7.99$): Maintain current difficulty.
- **Weak Performance** (Average score $< 5.0$): Reduce difficulty (`Hard` $\rightarrow$ `Medium` $\rightarrow$ `Easy`).

### 6. LLM Mode vs Offline Fallback Mode
When an LLM API key is configured, questions and evaluations are dynamically generated through LangChain. The offline simulation engine exists to allow offline testing and deterministic validation across all 10 supported domains without static fallback degradation.

### 7. Evaluation Fairness Requirements
Evaluations assess candidate text strictly for technical correctness, concept understanding, depth, and communication clarity. Demographic, personal, or non-technical traits are excluded from scoring.

---

## Known Limitations
- LLM response latency depends on the cloud API provider network speed.
- Live code execution requires a sandboxed runtime environment (out of scope for text-based evaluation).

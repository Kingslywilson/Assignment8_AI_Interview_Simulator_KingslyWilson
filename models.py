from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

VALID_DOMAINS = [
    "Python", "Java", "JavaScript", "Full Stack Development",
    "Data Structures & Algorithms", "SQL", "FastAPI",
    "Generative AI", "LangChain", "Machine Learning"
]

VALID_DIFFICULTIES = ["Easy", "Medium", "Hard"]

VALID_EXPERIENCE_LEVELS = [
    "Fresher", "0–1 Years", "1–3 Years", "3–5 Years", "5+ Years"
]

class InterviewConfig(BaseModel):
    domain: str = Field(..., description="Selected technical domain")
    difficulty: str = Field(..., description="Initial difficulty level: Easy, Medium, or Hard")
    experience_level: str = Field(..., description="Candidate experience level")
    total_questions: int = Field(default=5, ge=1, le=20, description="Target total questions")

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        if v not in VALID_DOMAINS:
            raise ValueError(f"Invalid domain '{v}'. Must be one of {VALID_DOMAINS}")
        return v

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        if v not in VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty '{v}'. Must be one of {VALID_DIFFICULTIES}")
        return v

    @field_validator("experience_level")
    @classmethod
    def validate_experience_level(cls, v: str) -> str:
        if v not in VALID_EXPERIENCE_LEVELS:
            raise ValueError(f"Invalid experience_level '{v}'. Must be one of {VALID_EXPERIENCE_LEVELS}")
        return v

class InterviewQuestion(BaseModel):
    question_id: str = Field(..., description="Unique question identifier")
    topic: str = Field(..., description="Technical topic area")
    difficulty: str = Field(..., description="Target difficulty level")
    question: str = Field(..., description="Question prompt text")
    expected_concepts: List[str] = Field(..., description="Key expected technical concepts")
    is_followup: bool = Field(default=False, description="Whether this is a follow-up question")

class AnswerAnalysis(BaseModel):
    technical_correctness: float = Field(..., ge=0.0, le=10.0)
    completeness: float = Field(..., ge=0.0, le=10.0)
    depth: float = Field(..., ge=0.0, le=10.0)
    clarity: float = Field(..., ge=0.0, le=10.0)
    relevance: float = Field(..., ge=0.0, le=10.0)
    demonstrated_concepts: List[str] = Field(default_factory=list)
    missing_concepts: List[str] = Field(default_factory=list)
    confidence_observation: str = Field( default="No specific confidence-related observation was available from the response.")
    feedback: str = Field(...)

class DifficultyAdaptation(BaseModel):
    previous_difficulty: str = Field(...)
    next_difficulty: str = Field(...)
    reasoning: str = Field(...)
    trigger_followup: bool = Field(default=False)

class QuestionEvaluation(BaseModel):
    question_id: str = Field(...)
    topic: str = Field(...)
    difficulty: str = Field(...)
    question: str = Field(...)
    candidate_answer: str = Field(...)
    technical_score: float = Field(..., ge=0.0, le=10.0)
    clarity_score: float = Field(..., ge=0.0, le=10.0)
    overall_score: float = Field(..., ge=0.0, le=10.0)
    strengths: List[str] = Field(default_factory=list)
    missing_concepts: List[str] = Field(default_factory=list)

class TopicPerformance(BaseModel):
    topic: str = Field(...)
    questions_asked: int = Field(...)
    average_score: float = Field(...)
    percentage: float = Field(...)

class FinalEvaluation(BaseModel):
    technical_score: float = Field(..., ge=0.0, le=100.0)
    communication_score: float = Field(..., ge=0.0, le=100.0)
    topic_performances: List[TopicPerformance] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    interview_outcome: str = Field(...)
    recommendation_reason: str = Field(...)

class InterviewReport(BaseModel):
    domain: str = Field(...)
    difficulty: str = Field(...)
    experience_level: str = Field(...)
    total_questions_asked: int = Field(...)
    topics_covered: List[str] = Field(default_factory=list)
    technical_score: float = Field(...)
    communication_score: float = Field(...)
    topic_performances: List[TopicPerformance] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    interview_outcome: str = Field(...)
    recommendation_reason: str = Field(...)
    question_evaluations: List[QuestionEvaluation] = Field(default_factory=list)

from typing import List, Set
from models import InterviewConfig, InterviewQuestion, QuestionEvaluation
from memory import InterviewMemory

class InterviewState:
    def __init__(self, config: InterviewConfig, session_id: str = "session_001"):
        self.session_id = session_id
        self.config = config
        self.current_difficulty = config.difficulty
        self.current_question_index = 0
        self.questions: List[InterviewQuestion] = []
        self.evaluations: List[QuestionEvaluation] = []
        self.topics_covered: Set[str] = set()
        self.missing_concepts_pool: List[str] = []
        self.memory = InterviewMemory(session_id=session_id)

    def record_question(self, question: InterviewQuestion):
        self.questions.append(question)
        self.topics_covered.add(question.topic)
        self.current_question_index += 1
        self.memory.add_question(question.question)

    def record_answer_and_evaluation(self, answer_text: str, evaluation: QuestionEvaluation):
        self.evaluations.append(evaluation)
        self.memory.add_answer(answer_text)
        for m in evaluation.missing_concepts:
            if m and m not in self.missing_concepts_pool:
                self.missing_concepts_pool.append(m)

    def get_recent_scores(self, count: int = 3) -> List[float]:
        if not self.evaluations:
            return []
        return [e.technical_score for e in self.evaluations[-count:]]

    def get_asked_questions_summary(self) -> str:
        if not self.questions:
            return "None"
        return "; ".join([f"Q{i+1} ({q.topic}): {q.question}" for i, q in enumerate(self.questions)])

    def get_topics_covered_summary(self) -> str:
        if not self.topics_covered:
            return "None"
        return ", ".join(sorted(list(self.topics_covered)))

    def is_complete(self) -> bool:
        return len(self.evaluations) >= self.config.total_questions

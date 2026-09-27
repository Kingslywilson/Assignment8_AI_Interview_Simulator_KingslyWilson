import os
from typing import Optional, Tuple
from models import InterviewConfig, InterviewQuestion, QuestionEvaluation, AnswerAnalysis, InterviewReport
from interview_state import InterviewState
from scoring import ScoringEngine
from chains.question_generator import QuestionGeneratorChain
from chains.answer_evaluator import AnswerEvaluatorChain
from chains.difficulty_adapter import DifficultyAdapterChain
from chains.followup_generator import FollowupGeneratorChain
from chains.final_evaluator import FinalEvaluatorChain
from chains.report_generator import ReportGeneratorChain

class InterviewEngine:
    def __init__(self, config: InterviewConfig, session_id: str = "session_001"):
        self.state = InterviewState(config, session_id=session_id)
        self.question_gen = QuestionGeneratorChain()
        self.answer_eval = AnswerEvaluatorChain()
        self.difficulty_adapt = DifficultyAdapterChain()
        self.followup_gen = FollowupGeneratorChain()
        self.final_eval = FinalEvaluatorChain()
        self.report_gen = ReportGeneratorChain()
        self.last_question: Optional[InterviewQuestion] = None
        self.last_analysis: Optional[AnswerAnalysis] = None
        self.trigger_followup: bool = False

    def get_next_question(self) -> InterviewQuestion:
        q_idx = self.state.current_question_index + 1
        q_id = f"Q{q_idx:03d}"

        if self.trigger_followup and self.last_question and self.last_analysis:
            self.trigger_followup = False
            q = self.followup_gen.generate(
                domain=self.state.config.domain,
                experience_level=self.state.config.experience_level,
                previous_question=self.last_question.question,
                candidate_answer=self.state.evaluations[-1].candidate_answer if self.state.evaluations else "",
                missing_concepts=self.last_analysis.missing_concepts,
                current_difficulty=self.state.current_difficulty,
                question_id=f"{q_id}_FU",
                topic=self.last_question.topic
            )
        else:
            q = self.question_gen.generate(
                domain=self.state.config.domain,
                difficulty=self.state.current_difficulty,
                experience_level=self.state.config.experience_level,
                questions_history=self.state.get_asked_questions_summary(),
                topics_covered=self.state.get_topics_covered_summary(),
                question_id=q_id
            )

        self.last_question = q
        self.state.record_question(q)
        return q

    def submit_answer(self, candidate_answer: str) -> Tuple[QuestionEvaluation, str]:
        if not self.last_question:
            raise RuntimeError("No active question to answer. Call get_next_question() first.")

        analysis = self.answer_eval.evaluate(
            domain=self.state.config.domain,
            experience_level=self.state.config.experience_level,
            question=self.last_question.question,
            expected_concepts=self.last_question.expected_concepts,
            candidate_answer=candidate_answer
        )
        self.last_analysis = analysis

        scores = ScoringEngine.calculate_question_score(analysis)

        strengths = analysis.demonstrated_concepts
        if not strengths and analysis.technical_correctness >= 5.0:
            strengths = ["Responded with valid technical terminology"]

        qe = QuestionEvaluation(
            question_id=self.last_question.question_id,
            topic=self.last_question.topic,
            difficulty=self.last_question.difficulty,
            question=self.last_question.question,
            candidate_answer=candidate_answer,
            technical_score=scores["technical_score"],
            clarity_score=scores["clarity_score"],
            overall_score=scores["overall_score"],
            strengths=strengths,
            missing_concepts=analysis.missing_concepts
        )

        self.state.record_answer_and_evaluation(candidate_answer, qe)

        recent_scores = self.state.get_recent_scores(count=3)
        adaptation = self.difficulty_adapt.adapt(
            current_difficulty=self.state.current_difficulty,
            recent_scores=recent_scores,
            last_analysis=analysis
        )

        self.state.current_difficulty = adaptation.next_difficulty
        self.trigger_followup = adaptation.trigger_followup

        return qe, adaptation.reasoning

    def complete_interview(self) -> InterviewReport:
        final_eval = self.final_eval.evaluate_interview(self.state.config, self.state.evaluations)
        topics = list(self.state.topics_covered)
        report = self.report_gen.generate_report(self.state.config, final_eval, self.state.evaluations, topics)
        self.report_gen.save_outputs(report, output_dir="outputs")
        return report

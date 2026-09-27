import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from models import FinalEvaluation, QuestionEvaluation, InterviewConfig
from scoring import ScoringEngine
from chains.question_generator import get_llm

class FinalEvaluatorChain:
    def __init__(self, prompt_path: str = "prompts/final_evaluation_prompt.txt"):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
        self.prompt = ChatPromptTemplate.from_template(template_text)
        self.llm = get_llm()

    def evaluate_interview(
        self,
        config: InterviewConfig,
        evaluations: List[QuestionEvaluation]
    ) -> FinalEvaluation:
        all_missing = []
        for e in evaluations:
            all_missing.extend(e.missing_concepts)

        deterministic_eval = ScoringEngine.calculate_final_evaluation(evaluations, all_missing)

        if self.llm is not None:
            try:
                structured_chain = self.prompt | self.llm.with_structured_output(FinalEvaluation, method="json_mode")
                eval_summary = "\n".join([
                    f"Q: {e.question} | Tech Score: {e.technical_score}/10 | Clarity: {e.clarity_score}/10 | Missing: {e.missing_concepts}"
                    for e in evaluations
                ])
                llm_eval = structured_chain.invoke({
                    "domain": config.domain,
                    "difficulty": config.difficulty,
                    "experience_level": config.experience_level,
                    "evaluation_summary": eval_summary
                })
                return FinalEvaluation(
                    technical_score=deterministic_eval.technical_score,
                    communication_score=deterministic_eval.communication_score,
                    topic_performances=deterministic_eval.topic_performances,
                    strengths=llm_eval.strengths or deterministic_eval.strengths,
                    areas_for_improvement=llm_eval.areas_for_improvement or deterministic_eval.areas_for_improvement,
                    improvement_suggestions=llm_eval.improvement_suggestions or deterministic_eval.improvement_suggestions,
                    interview_outcome=deterministic_eval.interview_outcome,
                    recommendation_reason=llm_eval.recommendation_reason or deterministic_eval.recommendation_reason
                )
            except Exception:
                return deterministic_eval

        return deterministic_eval

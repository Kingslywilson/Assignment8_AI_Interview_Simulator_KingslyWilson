import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from models import DifficultyAdaptation, AnswerAnalysis
from chains.question_generator import get_llm

class DifficultyAdapterChain:
    def __init__(self, prompt_path: str = "prompts/difficulty_adjustment_prompt.txt"):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
        self.prompt = ChatPromptTemplate.from_template(template_text)
        self.llm = get_llm()

    def adapt(
        self,
        current_difficulty: str,
        recent_scores: List[float],
        last_analysis: AnswerAnalysis
    ) -> DifficultyAdaptation:
        if self.llm is not None:
            try:
                structured_chain = self.prompt | self.llm.with_structured_output(
                  DifficultyAdaptation,
                  method="json_mode"
                )
                scores_str = ", ".join([str(s) for s in recent_scores]) if recent_scores else "None"
                return structured_chain.invoke({
                    "current_difficulty": current_difficulty,
                    "recent_scores": scores_str,
                    "last_feedback": last_analysis.feedback
                })
            except Exception:
                pass

        return self._adapt_fallback(current_difficulty, recent_scores, last_analysis)

    def _adapt_fallback(
        self,
        current_difficulty: str,
        recent_scores: List[float],
        last_analysis: AnswerAnalysis
    ) -> DifficultyAdaptation:
        difficulty_levels = ["Easy", "Medium", "Hard"]
        current_idx = difficulty_levels.index(current_difficulty) if current_difficulty in difficulty_levels else 1

        if not recent_scores:
            avg_score = last_analysis.technical_correctness
        else:
            avg_score = sum(recent_scores) / len(recent_scores)

        trigger_followup = False
        if len(last_analysis.missing_concepts) > 0 and last_analysis.technical_correctness >= 4.0:
            trigger_followup = True

        if avg_score >= 8.0:
            next_idx = min(current_idx + 1, 2)
            reasoning = f"Strong candidate performance (avg score: {round(avg_score, 1)}/10). Increasing difficulty to test depth."
        elif avg_score < 5.0:
            next_idx = max(current_idx - 1, 0)
            reasoning = f"Candidate struggled (avg score: {round(avg_score, 1)}/10). Lowering difficulty to foundational concepts."
        else:
            next_idx = current_idx
            reasoning = f"Consistent moderate performance (avg score: {round(avg_score, 1)}/10). Maintaining current difficulty."

        return DifficultyAdaptation(
            previous_difficulty=current_difficulty,
            next_difficulty=difficulty_levels[next_idx],
            reasoning=reasoning,
            trigger_followup=trigger_followup
        )

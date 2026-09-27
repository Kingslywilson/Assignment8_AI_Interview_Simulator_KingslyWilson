import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from models import InterviewQuestion
from chains.question_generator import get_llm

class FollowupGeneratorChain:
    def __init__(self, prompt_path: str = "prompts/followup_question_prompt.txt"):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
        self.prompt = ChatPromptTemplate.from_template(template_text)
        self.llm = get_llm()
    def generate(
    self,
    domain: str,
    experience_level: str,
    previous_question: str,
    candidate_answer: str,
    missing_concepts: List[str],
    current_difficulty: str = "Medium",
    question_id: str = "Q002_FU",
    topic: str = "Technical Probing"
) -> InterviewQuestion:

     if self.llm is not None:
        try:
            structured_chain = self.prompt | self.llm.with_structured_output(
                InterviewQuestion,
                method="json_mode"
            )

            q = structured_chain.invoke({
                "domain": domain,
                "experience_level": experience_level,
                "previous_question": previous_question,
                "candidate_answer": candidate_answer,
                "missing_concepts": ", ".join(missing_concepts)
                    if missing_concepts else "None",
                "current_difficulty": current_difficulty,
                "question_id": question_id,
                "topic": topic
            })

            q.is_followup = True

            if topic and topic != "Technical Probing":
                q.topic = topic

            return q
        except Exception:
            pass

     return self._generate_fallback(
        domain,
        previous_question,
        candidate_answer,
        missing_concepts,
        current_difficulty,
        question_id,
        topic
    )
    
    def _generate_fallback(
        self,
        domain: str,
        previous_question: str,
        candidate_answer: str,
        missing_concepts: List[str],
        current_difficulty: str,
        question_id: str,
        topic: str
    ) -> InterviewQuestion:
        if "decorator" in previous_question.lower() or "decorator" in candidate_answer.lower():
            followup_text = "Following up on your explanation of decorators: How do decorators with arguments work, and what problem does functools.wraps solve?"
            expected = ["decorators with arguments", "outer wrapper", "functools.wraps", "metadata preservation"]
        elif missing_concepts:
            concept = missing_concepts[0]
            followup_text = f"Building directly on your previous response about {previous_question.split('?')[0]}: can you elaborate specifically on how {concept} works and what trade-offs it involves?"
            expected = [concept, "implementation detail", "trade-offs"]
        else:
            followup_text = f"That was a solid explanation. Can you discuss how you would handle edge cases and performance considerations for this in production?"
            expected = ["edge cases", "performance optimization", "production deployment"]

        return InterviewQuestion(
            question_id=question_id,
            topic=topic,
            difficulty=current_difficulty,
            question=followup_text,
            expected_concepts=expected,
            is_followup=True
        )

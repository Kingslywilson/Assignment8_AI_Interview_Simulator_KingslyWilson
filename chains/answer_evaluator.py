import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from models import AnswerAnalysis
from chains.question_generator import get_llm

class AnswerEvaluatorChain:
    def __init__(self, prompt_path: str = "prompts/answer_evaluation_prompt.txt"):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
        self.prompt = ChatPromptTemplate.from_template(template_text)
        self.llm = get_llm()

    def evaluate(
        self,
        domain: str,
        experience_level: str,
        question: str,
        expected_concepts: List[str],
        candidate_answer: str
    ) -> AnswerAnalysis:
        if self.llm is not None:
            try:
                structured_chain = self.prompt | self.llm.with_structured_output(AnswerAnalysis, method="json_mode")
                return structured_chain.invoke({
                    "domain": domain,
                    "experience_level": experience_level,
                    "question": question,
                    "expected_concepts": ", ".join(expected_concepts),
                    "candidate_answer": candidate_answer
                })
            except Exception:
                pass

        return self._evaluate_fallback(question, expected_concepts, candidate_answer)

    def _evaluate_fallback(
        self,
        question: str,
        expected_concepts: List[str],
        candidate_answer: str
    ) -> AnswerAnalysis:
        ans_lower = candidate_answer.lower().strip()

        if ans_lower in ["i don't know", "i dont know", "don't know", "no idea", "not sure", "idk", "i do not know"]:
            return AnswerAnalysis(
                technical_correctness=0.0,
                completeness=0.0,
                depth=0.0,
                clarity=7.0,
                relevance=0.0,
                demonstrated_concepts=[],
                missing_concepts=expected_concepts,
                confidence_observation="Candidate explicitly acknowledged lack of knowledge on this topic.",
                feedback="Candidate stated they do not know the answer. No technical score awarded."
            )

        demonstrated = []
        missing = []
        for concept in expected_concepts:
            concept_lower = concept.lower()
            if concept_lower in ans_lower:
                demonstrated.append(concept)
            else:
                words = concept_lower.split()
                if len(words) > 1 and all(word in ans_lower for word in words):
                    demonstrated.append(concept)
                else:
                    missing.append(concept)

        if not demonstrated and not any(w in ans_lower for w in ["python", "java", "data", "code", "function", "class", "api", "query", "model", "join"]):
            return AnswerAnalysis(
                technical_correctness=0.0,
                completeness=0.0,
                depth=0.0,
                clarity=3.0,
                relevance=0.0,
                demonstrated_concepts=[],
                missing_concepts=expected_concepts,
                confidence_observation="Response was completely irrelevant to the technical question asked.",
                feedback="Response did not address the technical question. Zero technical credit awarded."
            )

        ratio = len(demonstrated) / max(len(expected_concepts), 1)

        if ratio >= 0.75:
            tech_score = 9.0
            comp_score = 8.5
            depth_score = 8.5
            clar_score = 8.5
            rel_score = 9.0
            obs = "Candidate gave a thorough and structured answer covering key expected concepts with strong depth."
            fb = f"Strong response addressing {', '.join(demonstrated)}."
        elif ratio >= 0.4:
            tech_score = 6.5
            comp_score = 6.0
            depth_score = 6.0
            clar_score = 7.0
            rel_score = 8.0
            obs = "Candidate demonstrated partial understanding but missed key implementation details."
            fb = f"Partial response covering {', '.join(demonstrated)}, missing {', '.join(missing)}."
        else:
            tech_score = 3.5
            comp_score = 3.0
            depth_score = 3.0
            clar_score = 6.0
            rel_score = 4.0
            obs = "Response had limited technical depth and missed several core concepts."
            fb = f"Weak answer. Missed concepts: {', '.join(missing)}."

        return AnswerAnalysis(
            technical_correctness=tech_score,
            completeness=comp_score,
            depth=depth_score,
            clarity=clar_score,
            relevance=rel_score,
            demonstrated_concepts=demonstrated,
            missing_concepts=missing,
            confidence_observation=obs,
            feedback=fb
        )

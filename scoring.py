from typing import List, Dict
from models import AnswerAnalysis, QuestionEvaluation, TopicPerformance, FinalEvaluation

class ScoringEngine:
    @staticmethod
    def calculate_question_score(analysis: AnswerAnalysis) -> Dict[str, float]:
        if analysis.technical_correctness == 0.0 or analysis.relevance == 0.0:
            tech_score = 0.0
            clarity_score = round(analysis.clarity, 2)
            overall_score = round(0.30 * clarity_score, 2)
        else:
            tech_score = round(
                (0.35 * analysis.technical_correctness) +
                (0.25 * analysis.completeness) +
                (0.20 * analysis.depth) +
                (0.10 * analysis.relevance) +
                (0.10 * analysis.clarity),
                2
            )
            clarity_score = round(analysis.clarity, 2)
            overall_score = round((0.70 * tech_score) + (0.30 * clarity_score), 2)

        return {
            "technical_score": tech_score,
            "clarity_score": clarity_score,
            "overall_score": overall_score
        }

    @staticmethod
    def calculate_topic_performances(evaluations: List[QuestionEvaluation]) -> List[TopicPerformance]:
        topic_map: Dict[str, List[float]] = {}
        for ev in evaluations:
            if ev.topic not in topic_map:
                topic_map[ev.topic] = []
            topic_map[ev.topic].append(ev.overall_score)

        results = []
        for topic, scores in topic_map.items():
            avg = sum(scores) / len(scores)
            pct = round((avg / 10.0) * 100.0, 1)
            results.append(
                TopicPerformance(
                    topic=topic,
                    questions_asked=len(scores),
                    average_score=round(avg, 2),
                    percentage=pct
                )
            )
        return results

    @staticmethod
    def calculate_final_evaluation(evaluations: List[QuestionEvaluation], all_missing_concepts: List[str]) -> FinalEvaluation:
        if not evaluations:
            return FinalEvaluation(
                technical_score=0.0,
                communication_score=0.0,
                topic_performances=[],
                strengths=["No questions answered"],
                areas_for_improvement=["Complete interview required"],
                improvement_suggestions=["Complete at least one question"],
                interview_outcome="Needs Further Preparation",
                recommendation_reason="Interview was not completed."
            )

        avg_tech = sum(e.technical_score for e in evaluations) / len(evaluations)
        technical_score = round(avg_tech * 10.0, 1)

        avg_clarity = sum(e.clarity_score for e in evaluations) / len(evaluations)
        communication_score = round(avg_clarity * 10.0, 1)

        topic_perfs = ScoringEngine.calculate_topic_performances(evaluations)

        strengths = []
        areas_for_improvement = []
        for e in evaluations:
            for s in e.strengths:
                if s and s not in strengths:
                    strengths.append(s)
            for m in e.missing_concepts:
                if m and m not in areas_for_improvement:
                    areas_for_improvement.append(m)

        if not strengths:
            strengths = ["Demonstrated fundamental participation in technical interview"]

        suggestions = []
        for missing in areas_for_improvement[:5]:
            suggestions.append(f"Review and practice concepts related to: {missing}")
        if not suggestions:
            suggestions.append("Continue exploring advanced real-world system architecture patterns.")

        if technical_score >= 85.0:
            outcome = "Strong Interview Performance"
            reason = f"Candidate demonstrated excellent technical depth ({technical_score}/100) and communication clarity ({communication_score}/100)."
        elif technical_score >= 70.0:
            outcome = "Good Interview Performance"
            reason = f"Candidate showed solid domain knowledge ({technical_score}/100) with minor conceptual gaps."
        elif technical_score >= 50.0:
            outcome = "Needs Further Technical Evaluation"
            reason = f"Candidate met basic requirements ({technical_score}/100) but demonstrated inconsistent depth across topics."
        else:
            outcome = "Needs Further Preparation"
            reason = f"Candidate struggled with key domain concepts ({technical_score}/100), requiring further preparation."

        return FinalEvaluation(
            technical_score=technical_score,
            communication_score=communication_score,
            topic_performances=topic_perfs,
            strengths=strengths[:7],
            areas_for_improvement=areas_for_improvement[:7],
            improvement_suggestions=suggestions[:5],
            interview_outcome=outcome,
            recommendation_reason=reason
        )

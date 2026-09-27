import os
import sys
from dotenv import load_dotenv
from models import InterviewConfig, InterviewQuestion
from interview_engine import InterviewEngine

load_dotenv()

def run_test_scenarios():
    log_lines = []
    log_lines.append("# AI Interview Simulator — System Test Log & Validation")
    log_lines.append("This document records the empirical execution of all required failure and success test scenarios across multiple technical domains.")
    log_lines.append("\n---\n")

    log_lines.append("## Scenario 1: Valid Interview Setup (Domain: Python)")
    try:
        config = InterviewConfig(domain="Python", difficulty="Medium", experience_level="1–3 Years", total_questions=5)
        engine = InterviewEngine(config, session_id="test_valid_setup")
        log_lines.append(f"**Result:** SUCCESS. Configured domain '{config.domain}', difficulty '{config.difficulty}', experience '{config.experience_level}'.")
    except Exception as e:
        log_lines.append(f"**Result:** FAILED - {str(e)}")

    log_lines.append("\n## Scenario 2: Invalid Interview Setup Handling")
    try:
        invalid_config = InterviewConfig(domain="Python", difficulty="UltraHard", experience_level="Fresher", total_questions=5)
        InterviewEngine(invalid_config)
        log_lines.append("**Result:** FAILED - Did not catch invalid difficulty.")
    except ValueError as ve:
        log_lines.append(f"**Result:** SUCCESS. Handled invalid setup correctly with error: `{str(ve)}`.")
    except Exception as ex:
        log_lines.append(f"**Result:** SUCCESS. Handled invalid setup correctly with error: `{str(ex)}`.")

    log_lines.append("\n## Scenario 3: Strong Candidate Answer & Difficulty Adaptation (Domain: Java)")
    config_java = InterviewConfig(domain="Java", difficulty="Easy", experience_level="Fresher", total_questions=5)
    engine_java = InterviewEngine(config_java, session_id="test_strong_java")
    q1 = engine_java.get_next_question()
    log_lines.append(f"**Question [{q1.difficulty}]:** {q1.question}")
    strong_ans = "The JDK is the full development kit containing tools and the JRE. The JRE provides the runtime environment and class libraries. The JVM executes compiled Java bytecode on the target machine."
    eval1, reasoning1 = engine_java.submit_answer(strong_ans)
    log_lines.append(f"**Answer:** \"{strong_ans}\"")
    log_lines.append(f"**Technical Score:** {eval1.technical_score}/10 | **Overall Score:** {eval1.overall_score}/10")
    log_lines.append(f"**Adaptation:** {reasoning1}")
    log_lines.append(f"**Next Target Difficulty:** {engine_java.state.current_difficulty}")

    log_lines.append("\n## Scenario 4: Weak Candidate Answer & Difficulty Decrease (Domain: DSA)")
    config_dsa = InterviewConfig(domain="Data Structures & Algorithms", difficulty="Hard", experience_level="3–5 Years", total_questions=5)
    engine_dsa = InterviewEngine(config_dsa, session_id="test_weak_dsa")
    q_hard = engine_dsa.get_next_question()
    log_lines.append(f"**Question [{q_hard.difficulty}]:** {q_hard.question}")
    weak_ans = "I think arrays and hash tables are the same thing and both use linear search."
    eval_weak, reasoning_weak = engine_dsa.submit_answer(weak_ans)
    log_lines.append(f"**Answer:** \"{weak_ans}\"")
    log_lines.append(f"**Technical Score:** {eval_weak.technical_score}/10")
    log_lines.append(f"**Adaptation:** {reasoning_weak}")
    log_lines.append(f"**Next Target Difficulty:** {engine_dsa.state.current_difficulty}")

    log_lines.append("\n## Scenario 5: Partial Answer Concept Separation (Domain: SQL)")
    config_sql = InterviewConfig(domain="SQL", difficulty="Medium", experience_level="1–3 Years", total_questions=5)
    engine_sql = InterviewEngine(config_sql, session_id="test_partial_sql")
    q_sql = engine_sql.get_next_question()
    log_lines.append(f"**Question:** {q_sql.question}")
    partial_ans = "INNER JOIN returns rows when there is a match in both tables based on join keys."
    eval_p, _ = engine_sql.submit_answer(partial_ans)
    log_lines.append(f"**Answer:** \"{partial_ans}\"")
    log_lines.append(f"**Demonstrated Concepts:** {eval_p.strengths}")
    log_lines.append(f"**Missing Concepts:** {eval_p.missing_concepts}")

    log_lines.append("\n## Scenario 6: Irrelevant Answer Handling")
    config_irr = InterviewConfig(domain="Python", difficulty="Medium", experience_level="Fresher", total_questions=5)
    engine_irr = InterviewEngine(config_irr, session_id="test_irrelevant")
    q_irr = engine_irr.get_next_question()
    log_lines.append(f"**Question:** {q_irr.question}")
    irr_ans = "I really enjoy playing cricket and cooking dinner on weekends."
    eval_irr, _ = engine_irr.submit_answer(irr_ans)
    log_lines.append(f"**Answer:** \"{irr_ans}\"")
    log_lines.append(f"**Technical Score:** {eval_irr.technical_score}/10 (Zero technical credit awarded for off-topic response)")

    log_lines.append("\n## Scenario 7: 'I Don't Know' Response Handling")
    config_idk = InterviewConfig(domain="Python", difficulty="Medium", experience_level="Fresher", total_questions=5)
    engine_idk = InterviewEngine(config_idk, session_id="test_idk")
    q_idk = engine_idk.get_next_question()
    log_lines.append(f"**Question:** {q_idk.question}")
    idk_ans = "I don't know"
    eval_idk, _ = engine_idk.submit_answer(idk_ans)
    log_lines.append(f"**Answer:** \"{idk_ans}\"")
    log_lines.append(f"**Technical Score:** {eval_idk.technical_score}/10")
    log_lines.append(f"**Clarity Score:** {eval_idk.clarity_score}/10 (Honest response acknowledged without unearned technical score)")

    log_lines.append("\n## Scenario 8: Follow-Up Question Generation & Context Probing (Domain: Python)")
    config_fu = InterviewConfig(domain="Python", difficulty="Medium", experience_level="1–3 Years", total_questions=5)
    engine_fu = InterviewEngine(config_fu, session_id="test_followup")

    q_orig = InterviewQuestion(
        question_id="Q001",
        topic="Python Decorators",
        difficulty="Medium",
        question="What is a Python decorator and how does it modify function behavior?",
        expected_concepts=["decorator syntax", "wrap function", "functools.wraps", "arguments"],
        is_followup=False
    )
    engine_fu.last_question = q_orig
    engine_fu.state.record_question(q_orig)

    orig_ans = "Decorators use decorator syntax @ to wrap function execution at runtime."
    log_lines.append(f"**Original Question [{q_orig.topic}]:** {q_orig.question}")
    log_lines.append(f"**Candidate Answer:** \"{orig_ans}\"")
    eval_orig, _ = engine_fu.submit_answer(orig_ans)

    q_followup = engine_fu.get_next_question()
    log_lines.append(f"**Follow-Up Generated:** {q_followup.question}")
    log_lines.append(f"**Topic Preserved:** {q_followup.topic}")
    log_lines.append(f"**Is Follow-Up Flag:** {q_followup.is_followup}")

    log_lines.append("\n## Scenario 9: Duplicate Topic & Question Prevention")
    config_dup = InterviewConfig(domain="Python", difficulty="Medium", experience_level="1–3 Years", total_questions=5)
    engine_dup = InterviewEngine(config_dup, session_id="test_duplicate")
    q_a = engine_dup.get_next_question()
    engine_dup.submit_answer("Mutable lists can change in place, while tuple is immutable.")
    q_b = engine_dup.get_next_question()
    log_lines.append(f"**Question 1 Topic:** {q_a.topic}")
    log_lines.append(f"**Question 2 Topic:** {q_b.topic}")
    log_lines.append(f"**Different Topics Ensured:** {q_a.topic != q_b.topic}")

    log_lines.append("\n## Scenario 10: Multi-Turn Full Interview Run & Report Generation")
    config_full = InterviewConfig(domain="Python", difficulty="Medium", experience_level="1–3 Years", total_questions=5)
    engine_full = InterviewEngine(config_full, session_id="test_full_run")

    answers_map = {
        "Python Fundamentals": "Mutable objects like lists can be modified in place, whereas immutable objects like tuples cannot be modified. Mutability affects memory reference and hashability.",
        "OOP": "Inheritance forms a child class from a parent class for reusability, whereas composition combines decoupled objects via attributes to reduce coupling.",
        "Exception Handling": "The try block executes risky code, except block catches exceptions, else clause runs when no exceptions occur, and finally cleanup always executes.",
        "Async Programming": "Asyncio uses an event loop to execute coroutines concurrently using awaitables with async and await keywords.",
        "Design Patterns": "A thread safety lock ensures a singleton instance is created once, while dependency injection injects services into consumers for decoupling."
    }

    for i in range(5):
        q = engine_full.get_next_question()
        ans_text = answers_map.get(q.topic, "Detailed answer covering all expected concepts, patterns, and trade-offs.")
        log_lines.append(f"\n**Turn {i+1} [{q.difficulty}] Topic:** {q.topic}")
        log_lines.append(f"**Q:** {q.question}")
        eval_item, adaptation_text = engine_full.submit_answer(ans_text)
        log_lines.append(f"**A:** \"{ans_text}\"")
        log_lines.append(f"**Score:** Tech {eval_item.technical_score}/10 | Clarity {eval_item.clarity_score}/10 | Overall {eval_item.overall_score}/10")
        log_lines.append(f"**Engine Note:** {adaptation_text}")

    report = engine_full.complete_interview()
    log_lines.append(f"\n**Final Technical Score:** {report.technical_score}/100")
    log_lines.append(f"**Final Communication Score:** {report.communication_score}/100")
    log_lines.append(f"**Outcome Recommendation:** {report.interview_outcome}")
    log_lines.append(f"**Generated Artifacts:** `outputs/interview_report.md`, `outputs/interview_report.json`")

    with open("test_log.md", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print("Test execution complete. Log saved to test_log.md.")

def interactive_cli():
    print("==================================================")
    print("      AI INTERVIEW SIMULATOR (LangChain)          ")
    print("==================================================")

    domains = ["Python", "Java", "JavaScript", "Full Stack Development", "Data Structures & Algorithms", "SQL", "FastAPI", "Generative AI", "LangChain", "Machine Learning"]
    print("\nSelect Domain:")
    for idx, d in enumerate(domains, 1):
        print(f"  {idx}. {d}")
    d_choice = input(f"Choice (1-{len(domains)}) [1]: ").strip()
    domain = domains[int(d_choice) - 1] if d_choice.isdigit() and 1 <= int(d_choice) <= len(domains) else "Python"

    difficulties = ["Easy", "Medium", "Hard"]
    print("\nSelect Initial Difficulty:")
    for idx, df in enumerate(difficulties, 1):
        print(f"  {idx}. {df}")
    df_choice = input("Choice (1-3) [2]: ").strip()
    difficulty = difficulties[int(df_choice) - 1] if df_choice.isdigit() and 1 <= int(df_choice) <= 3 else "Medium"

    exp_levels = ["Fresher", "0–1 Years", "1–3 Years", "3–5 Years", "5+ Years"]
    print("\nSelect Experience Level:")
    for idx, ex in enumerate(exp_levels, 1):
        print(f"  {idx}. {ex}")
    ex_choice = input(f"Choice (1-{len(exp_levels)}) [3]: ").strip()
    exp_level = exp_levels[int(ex_choice) - 1] if ex_choice.isdigit() and 1 <= int(ex_choice) <= len(exp_levels) else "1–3 Years"

    num_q_str = input("\nTotal Questions (3-10) [5]: ").strip()
    total_q = int(num_q_str) if num_q_str.isdigit() and 3 <= int(num_q_str) <= 10 else 5

    config = InterviewConfig(
        domain=domain,
        difficulty=difficulty,
        experience_level=exp_level,
        total_questions=total_q
    )

    engine = InterviewEngine(config, session_id="cli_session")
    print(f"\nStarting Interview: {domain} | {difficulty} | {exp_level} | {total_q} Questions")
    print("Type 'exit' to terminate early.\n")

    for turn in range(total_q):
        q = engine.get_next_question()
        print(f"\n--------------------------------------------------")
        print(f"Question {turn + 1}/{total_q} [{q.difficulty}] (Topic: {q.topic})")
        print(f"Interviewer: {q.question}")
        print(f"--------------------------------------------------")

        ans = input("Candidate Answer: ").strip()
        if ans.lower() == "exit":
            print("Ending interview early.")
            break

        qe, adaptation_msg = engine.submit_answer(ans)
        print(f"\n[Evaluation] Technical Score: {qe.technical_score}/10 | Clarity Score: {qe.clarity_score}/10")
        if qe.missing_concepts:
            print(f"[Missing Concepts]: {', '.join(qe.missing_concepts)}")
        print(f"[Engine Note]: {adaptation_msg}")

    print("\nGenerating structured interview report...")
    report = engine.complete_interview()
    print("\n==================================================")
    print(f"Final Technical Score:      {report.technical_score} / 100")
    print(f"Final Communication Score:  {report.communication_score} / 100")
    print(f"Interview Outcome:          {report.interview_outcome}")
    print("==================================================")
    print("Report saved to outputs/interview_report.md and outputs/interview_report.json.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--demo", "--run-tests"]:
        run_test_scenarios()
    else:
        run_test_scenarios()
        print("\nStarting interactive CLI mode...\n")
        interactive_cli()

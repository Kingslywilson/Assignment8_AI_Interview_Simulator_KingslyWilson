# AI Interview Simulator — System Test Log & Validation
This document records the empirical execution of all required failure and success test scenarios across multiple technical domains.

---

## Scenario 1: Valid Interview Setup (Domain: Python)
**Result:** SUCCESS. Configured domain 'Python', difficulty 'Medium', experience '1–3 Years'.

## Scenario 2: Invalid Interview Setup Handling
**Result:** SUCCESS. Handled invalid setup correctly with error: `1 validation error for InterviewConfig
difficulty
  Value error, Invalid difficulty 'UltraHard'. Must be one of ['Easy', 'Medium', 'Hard'] [type=value_error, input_value='UltraHard', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error`.

## Scenario 3: Strong Candidate Answer & Difficulty Adaptation (Domain: Java)
**Question [Easy]:** In Java, how do you declare a variable to store the number of students in a class, and which primitive data type would you choose? Write the declaration statement and explain why that type is appropriate.
**Answer:** "The JDK is the full development kit containing tools and the JRE. The JRE provides the runtime environment and class libraries. The JVM executes compiled Java bytecode on the target machine."
**Technical Score:** 3.58/10 | **Overall Score:** 4.31/10
**Adaptation:** Candidate struggled (avg score: 3.6/10). Lowering difficulty to foundational concepts.
**Next Target Difficulty:** Easy

## Scenario 4: Weak Candidate Answer & Difficulty Decrease (Domain: DSA)
**Question [Hard]:** Explain how hash table collisions are resolved in dynamic arrays and dictionaries.
**Answer:** "I think arrays and hash tables are the same thing and both use linear search."
**Technical Score:** 0.0/10
**Adaptation:** Candidate struggled (avg score: 0.0/10). Lowering difficulty to foundational concepts.
**Next Target Difficulty:** Medium

## Scenario 5: Partial Answer Concept Separation (Domain: SQL)
**Question:** Write an SQL query to retrieve the employee_name and salary of the employee who earns the second highest salary in each department. The schema includes an Employees table (employee_id, employee_name, department_id) and a Salaries table (employee_id, salary). Return results only for departments that have at least two employees.
**Answer:** "INNER JOIN returns rows when there is a match in both tables based on join keys."
**Demonstrated Concepts:** []
**Missing Concepts:** ['JOIN between Employees and Salaries', 'WINDOW functions such as DENSE_RANK or ROW_NUMBER partitioned by department_id', 'ORDER BY salary DESC within the window', 'Filtering the window rank to = 2', 'Handling ties and ensuring departments have >=2 employees']

## Scenario 6: Irrelevant Answer Handling
**Question:** What is the difference between mutable and immutable data types in Python? Give examples.
**Answer:** "I really enjoy playing cricket and cooking dinner on weekends."
**Technical Score:** 0.0/10 (Zero technical credit awarded for off-topic response)

## Scenario 7: 'I Don't Know' Response Handling
**Question:** What is the difference between mutable and immutable data types in Python? Give examples.
**Answer:** "I don't know"
**Technical Score:** 0.0/10
**Clarity Score:** 7.0/10 (Honest response acknowledged without unearned technical score)

## Scenario 8: Follow-Up Question Generation & Context Probing (Domain: Python)
**Original Question [Python Decorators]:** What is a Python decorator and how does it modify function behavior?
**Candidate Answer:** "Decorators use decorator syntax @ to wrap function execution at runtime."
**Follow-Up Generated:** Following up on your explanation of decorators: How do decorators with arguments work, and what problem does functools.wraps solve?
**Topic Preserved:** Python Decorators
**Is Follow-Up Flag:** True

## Scenario 9: Duplicate Topic & Question Prevention
**Question 1 Topic:** Python Fundamentals
**Question 2 Topic:** OOP
**Different Topics Ensured:** True

## Scenario 10: Multi-Turn Full Interview Run & Report Generation

**Turn 1 [Medium] Topic:** Python Fundamentals
**Q:** What is the difference between mutable and immutable data types in Python? Give examples.
**A:** "Mutable objects like lists can be modified in place, whereas immutable objects like tuples cannot be modified. Mutability affects memory reference and hashability."
**Score:** Tech 8.73/10 | Clarity 8.5/10 | Overall 8.66/10
**Engine Note:** Strong candidate performance (avg score: 8.7/10). Increasing difficulty to test depth.

**Turn 2 [Hard] Topic:** Python Fundamentals
**Q:** Building directly on your previous response about What is the difference between mutable and immutable data types in Python: can you elaborate specifically on how lists vs tuples works and what trade-offs it involves?
**A:** "Mutable objects like lists can be modified in place, whereas immutable objects like tuples cannot be modified. Mutability affects memory reference and hashability."
**Score:** Tech 0.0/10 | Clarity 3.0/10 | Overall 0.9/10
**Engine Note:** Candidate struggled (avg score: 4.4/10). Lowering difficulty to foundational concepts.

**Turn 3 [Medium] Topic:** OOP
**Q:** Explain inheritance and composition in Python. When would you prefer composition?
**A:** "Inheritance forms a child class from a parent class for reusability, whereas composition combines decoupled objects via attributes to reduce coupling."
**Score:** Tech 8.73/10 | Clarity 8.5/10 | Overall 8.66/10
**Engine Note:** Consistent moderate performance (avg score: 5.8/10). Maintaining current difficulty.

**Turn 4 [Medium] Topic:** Exception Handling
**Q:** How does exception handling work in Python with try-except-else-finally blocks?
**A:** "The try block executes risky code, except block catches exceptions, else clause runs when no exceptions occur, and finally cleanup always executes."
**Score:** Tech 8.73/10 | Clarity 8.5/10 | Overall 8.66/10
**Engine Note:** Consistent moderate performance (avg score: 5.8/10). Maintaining current difficulty.

**Turn 5 [Medium] Topic:** Async Programming
**Q:** Explain async/await and event loops in Python asyncio.
**A:** "Asyncio uses an event loop to execute coroutines concurrently using awaitables with async and await keywords."
**Score:** Tech 8.73/10 | Clarity 8.5/10 | Overall 8.66/10
**Engine Note:** Strong candidate performance (avg score: 8.7/10). Increasing difficulty to test depth.

**Final Technical Score:** 69.8/100
**Final Communication Score:** 74.0/100
**Outcome Recommendation:** Needs Further Technical Evaluation
**Generated Artifacts:** `outputs/interview_report.md`, `outputs/interview_report.json`
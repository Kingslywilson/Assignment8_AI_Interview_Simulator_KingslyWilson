import os
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from models import InterviewQuestion

def get_llm():
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if groq_key:
        from langchain_groq import ChatGroq
        return ChatGroq(model_name="openai/gpt-oss-120b", api_key=groq_key, temperature=0.3)


class QuestionGeneratorChain:
    def __init__(self, prompt_path: str = "prompts/question_generation_prompt.txt"):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
        self.prompt = ChatPromptTemplate.from_template(template_text)
        self.llm = get_llm()

    def generate(
        self,
        domain: str,
        difficulty: str,
        experience_level: str,
        questions_history: str,
        topics_covered: str,
        question_id: str = "Q001"
    ) -> InterviewQuestion:
        if self.llm is not None:
            try:
                structured_chain = self.prompt | self.llm.with_structured_output(
                    InterviewQuestion,
                    method="json_mode"
                )
                return structured_chain.invoke({
                    "domain": domain,
                    "difficulty": difficulty,
                    "experience_level": experience_level,
                    "questions_history": questions_history,
                    "topics_covered": topics_covered
                })
            except Exception:
                pass

        return self._generate_fallback(domain, difficulty, experience_level, questions_history, topics_covered, question_id)

    def _generate_fallback(
        self,
        domain: str,
        difficulty: str,
        experience_level: str,
        questions_history: str,
        topics_covered: str,
        question_id: str
    ) -> InterviewQuestion:
        bank = {
            "Python": [
                ("Python Fundamentals", "What is the difference between mutable and immutable data types in Python? Give examples.", ["mutability", "lists vs tuples", "memory reference", "hashability"]),
                ("OOP", "Explain inheritance and composition in Python. When would you prefer composition?", ["inheritance", "composition", "coupling", "reusability"]),
                ("Exception Handling", "How does exception handling work in Python with try-except-else-finally blocks?", ["try block", "except block", "else clause", "finally cleanup"]),
                ("Async Programming", "Explain async/await and event loops in Python asyncio.", ["asyncio", "event loop", "coroutines", "awaitables"]),
                ("Design Patterns", "How would you design a thread-safe Singleton pattern or dependency injection in Python?", ["singleton", "thread safety", "dependency injection", "decoupling"])
            ],
            "Java": [
                ("Java Core", "Explain the difference between JVM, JRE, and JDK, and how bytecode execution works.", ["JVM", "JRE", "JDK", "bytecode"]),
                ("OOP Concepts", "How does method overriding differ from method overloading in Java?", ["overloading", "overriding", "polymorphism", "compile-time vs runtime"]),
                ("Concurrency", "Explain synchronized blocks and volatile variables in Java multithreading.", ["synchronized", "volatile", "thread safety", "memory visibility"]),
                ("Spring Framework", "How does Dependency Injection and Inversion of Control work in Spring Boot?", ["IoC container", "Dependency Injection", "Beans", "Autowiring"])
            ],
            "JavaScript": [
                ("JS Engine", "Explain the event loop, call stack, and microtask queue in JavaScript.", ["event loop", "call stack", "microtask queue", "promises"]),
                ("Closures", "What is a closure in JavaScript and how does lexical scoping enable it?", ["closure", "lexical scope", "encapsulation", "variable scope"]),
                ("Async JS", "Compare Promises and Async/Await in modern JavaScript.", ["promises", "async await", "error handling", "non-blocking"])
            ],
            "Full Stack Development": [
                ("Architecture", "How would you design an end-to-end web application with authentication and state management?", ["REST API", "JWT auth", "frontend state", "database design"]),
                ("Performance", "What strategies do you use to optimize web application loading speed and database queries?", ["caching", "lazy loading", "indexing", "CDN"])
            ],
            "Data Structures & Algorithms": [
                ("Arrays & Hash Tables", "Explain how hash table collisions are resolved in dynamic arrays and dictionaries.", ["hash function", "collisions", "chaining", "open addressing"]),
                ("Trees & Graphs", "Compare Depth-First Search (DFS) and Breadth-First Search (BFS) in terms of space and time complexity.", ["DFS", "BFS", "queue", "stack", "time complexity"]),
                ("Dynamic Programming", "What is overlapping subproblems property and how does memoization optimize recursive algorithms?", ["dp", "memoization", "recursion", "subproblems"])
            ],
            "SQL": [
                ("Relational Model", "Explain INNER JOIN, LEFT JOIN, and FULL OUTER JOIN with practical use cases.", ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "practical use cases"]),
                ("Indexing", "How do B-Tree indexes accelerate SELECT queries and what are their trade-offs during WRITE operations?", ["B-Tree", "indexes", "query optimization", "write latency"]),
                ("Transactions & ACID", "Explain isolation levels and ACID properties in relational database transactions.", ["ACID", "isolation levels", "concurrency", "locking"]),
                ("Query Optimization", "How do EXPLAIN execution plans help identify slow SQL queries and full table scans?", ["execution plan", "EXPLAIN", "table scan", "cost optimization"])
            ],
            "FastAPI": [
                ("API Routing", "How does Pydantic data validation and Dependency Injection work in FastAPI endpoints?", ["Pydantic models", "Depends()", "type annotations", "request validation"]),
                ("Async Endpoints", "When should you declare a FastAPI path operation function with async def vs regular def?", ["async def", "thread pool", "concurrency", "blocking IO"])
            ],
            "Generative AI": [
                ("LLM Architecture", "Explain the Transformer architecture attention mechanism and tokenization pipeline.", ["self-attention", "tokenization", "embeddings", "transformers"]),
                ("RAG", "How does Retrieval-Augmented Generation (RAG) mitigate LLM hallucinations?", ["vector store", "embeddings", "context augmentation", "hallucinations"])
            ],
            "LangChain": [
                ("Chains & LCEL", "Explain LangChain Expression Language (LCEL) and how Runnables are composed.", ["LCEL", "Runnables", "chaining", "pipe operator"]),
                ("Memory & Agents", "How do tools and agents interact in LangChain to handle complex multi-step reasoning?", ["Agents", "Tools", "ReAct loop", "ChatHistory"])
            ],
            "Machine Learning": [
                ("Model Evaluation", "Explain Bias-Variance tradeoff, Precision, Recall, and F1-Score.", ["bias variance", "precision", "recall", "overfitting"]),
                ("Gradient Descent", "How does gradient descent optimize loss functions in neural networks?", ["gradient descent", "loss function", "learning rate", "backpropagation"])
            ]
        }

        domain_questions = bank.get(domain, bank["Python"])
        for topic, text, concepts in domain_questions:
            if topic not in topics_covered and text not in questions_history:
                return InterviewQuestion(
                    question_id=question_id,
                    topic=topic,
                    difficulty=difficulty,
                    question=text,
                    expected_concepts=concepts,
                    is_followup=False
                )

        asked_count = len([q for q in questions_history.split(";") if q.strip()])
        base_topic, base_text, base_concepts = domain_questions[asked_count % len(domain_questions)]
        variation_topic = f"{base_topic} Scenario"
        variation_text = f"In the context of {base_topic} ({difficulty} level): How would you approach handling production trade-offs and edge cases for {base_concepts[0]}?"
        variation_concepts = [f"{base_concepts[0]} trade-offs", "edge cases", "production resilience"]

        return InterviewQuestion(
            question_id=question_id,
            topic=variation_topic,
            difficulty=difficulty,
            question=variation_text,
            expected_concepts=variation_concepts,
            is_followup=False
        )

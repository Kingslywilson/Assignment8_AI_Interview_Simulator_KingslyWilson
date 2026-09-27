from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class InterviewMemory:
    def __init__(self, session_id: str = "default_session"):
        self.session_id = session_id
        self.messages: List[BaseMessage] = []

    def add_question(self, question_text: str):
        self.messages.append(AIMessage(content=f"Interviewer: {question_text}"))

    def add_answer(self, answer_text: str):
        self.messages.append(HumanMessage(content=f"Candidate: {answer_text}"))

    def get_messages(self) -> List[BaseMessage]:
        return self.messages

    def get_formatted_history(self) -> str:
        if not self.messages:
            return "No previous conversation."
        formatted = []
        for msg in self.messages:
            role = "Interviewer" if isinstance(msg, AIMessage) else "Candidate"
            formatted.append(f"{role}: {msg.content}")
        return "\n".join(formatted)

    def clear(self):
        self.messages.clear()


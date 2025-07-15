from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.model.groq_llm import GroqLLM
from app.core.config import GROQ_API_KEY
from app.services.user_state import get_user_topics, get_next_topic, update_user_topics

class CorrectionChainService:
    def __init__(self):
        self.llm = GroqLLM(api_key=GROQ_API_KEY)

        self.correction_prompt = PromptTemplate(
            input_variables=["bangla_sentence", "user_translation"],
            template="""
                You are an IELTS English tutor helping Bangladeshi students.

                Step 1: The AI provides a Bangla sentence:  
                "{bangla_sentence}"

                Step 2: The student translated it as:  
                "{user_translation}"

                Now do the following:
                1. Check if the English sentence is grammatically correct and natural for IELTS.
                2. If wrong, provide a corrected version.
                3. Mention which grammar topic it relates to and its gramatical structure.
                4. Explain the mistake in simple Bangla.
                5. Rate the sentence from 1 to 9 (IELTS band scale).
                6. Suggest synonyms words or most appropiate word for this sentence.

                Use this format:

                ✅ Corrected Sentence: ...
                📘 Explanation (Bangla): ...
                📊 IELTS Band Score: ...
            """
        )

        self.bangla_gen_prompt = PromptTemplate(
            input_variables=["user_id", "previous_topics", "next_topic"],
            template="""
                You are a Bangla grammar teacher helping IELTS students improve their English.

                Each sentence should:
                - Be written in **Bangla only**
                - Focus on the grammar topic: "{next_topic}"
                - Avoid repeating topics already used: {previous_topics}
                - Be short and practical for IELTS preparation

                Now generate a **new Bangla sentence** that tests the topic "{next_topic}".
            """
        )

        self.correction_chain = LLMChain(llm=self.llm, prompt=self.correction_prompt)
        self.bangla_gen_chain = LLMChain(llm=self.llm, prompt=self.bangla_gen_prompt)

    def generate_bangla_sentence(self, user_id: int) -> str:
        previous_topics = get_user_topics(user_id)
        next_topic = get_next_topic(user_id)
        if not next_topic:
            return "✅ All grammar topics are completed. Great job!"

        result = self.bangla_gen_chain.run({
            "user_id": str(user_id),
            "previous_topics": ", ".join(previous_topics) or "None",
            "next_topic": next_topic
        })
        update_user_topics(user_id, next_topic)
        return result.strip()

    def get_correction(self, bangla_sentence: str, user_translation: str) -> str:
        return self.correction_chain.run({
            "bangla_sentence": bangla_sentence,
            "user_translation": user_translation,
        })

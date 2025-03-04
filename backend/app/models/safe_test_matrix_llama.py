import openai
import numpy as np

class SafeTestMatrixLlama:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_warning(self, risk_score):
        if risk_score < 0.3:
            return "No significant risk detected."
        elif risk_score < 0.7:
            return "Medium risk detected. Please be cautious."
        else:
            return "High risk detected. Immediate action required."

    def generate_explanation(self, risk_score):
        if risk_score < 0.3:
            return "No significant risk detected."
        elif risk_score < 0.7:
            return "Medium risk detected. Please be cautious."
        else:
            return "High risk detected. Immediate action required."

    def interface_with_llm(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

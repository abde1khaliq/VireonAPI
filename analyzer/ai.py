import re
import json
import html
import google.generativeai as genai
from decouple import config

genai.configure(api_key=config('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-2.5-flash-lite")


class ModerationService:
    def clean_content(self, content: str):
        content = html.unescape(content)
        content = re.sub(r'\s+', " ", content).strip()
        content = content.replace("\\n", " ").replace("\\t", " ")
        content = re.sub(r"(.)\1{2,}", r"\1\1", content)
        return content

    def build_prompt(self, content: str):
        return (
            f"You are a strict moderation assistant. Evaluate the following input: '{content}'.\n"
            "Focus entirely on the content itself and the word. Identify potential harm including profanity, hate speech, threats, or sexually explicit language.\n"
            "Also focus on the arabic franko. and so on.\n"
            "Respond only with valid JSON in this format:\n"
            "{\n"
            '  "violation": boolean,\n'
            '  "harm_type": list of strings,\n'
            '  "confidence": float (0 to 1),\n'
            '  "severity": "low" | "moderate" | "high",\n'
            '  "reasoning": string (only include if violation is true)\n'
            "}"
        )

    def call_model(self, prompt, raw=None):
        response = model.generate_content(prompt)
        raw_text = response.text or response.parts[0].text
        json_block = re.sub(r"```json|```", "", raw_text).strip()
        result = json.loads(json_block)
        return {"result": result}

    def moderate(self, content, content_type: str):
        if content_type == "text":
            cleaned = self.clean_content(content)
            prompt = self.build_prompt(cleaned)
            return self.call_model(prompt, raw=cleaned)

        elif content_type == "image":
            return self.analyze_image(content)

        else:
            return {"error": f"Unsupported content type: {content_type}"}


    def analyze_image(self, image_file):
        try:
            image_bytes = image_file.read()
            prompt = (
                "You are a strict moderation assistant. Evaluate the visual content of the attached image.\n"
                "Identify harmful content such as hate symbols, graphic violence, or sexually explicit imagery.\n"
                "Respond only with valid JSON in this format:\n"
                "{\n"
                '  "violation": boolean,\n'
                '  "harm_type": list of strings,\n'
                '  "confidence": float (0 to 1),\n'
                '  "severity": "low" | "moderate" | "high",\n'
                '  "reasoning": string (only include if violation is true)\n'
                "}"
            )

            response = model.generate_content(
                [
                    prompt,
                    {"mime_type": image_file.content_type, "data": image_bytes}
                ]
            )

            raw_text = response.text or response.parts[0].text
            json_block = re.sub(r"```json|```", "", raw_text).strip()
            result = json.loads(json_block)

        except Exception as e:
            return {
                "error": "Image moderation failed",
                "details": str(e),
            }

        return {"result": result}

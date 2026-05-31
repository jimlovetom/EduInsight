import json
from pathlib import Path


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_prompt(file_path):
    """Load prompt template from a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def mock_ai_analysis(student_data, prompt_template):
    """
    Mock AI analysis function.
    This simulates what an LLM would output based on the input data.
    """

    student_id = student_data["student_profile"]["student_id"]
    subject = student_data["subject"]["name"]
    grade = student_data["student_profile"]["grade"]

    weak_points = [
        kp["knowledge_point"]
        for kp in student_data["knowledge_mastery"]
        if kp["mastery_level"] in ["weak", "basic"]
    ]

    analysis_result = f"""
AI LEARNING ANALYSIS REPORT (Mock Version)

Student ID: {student_id}
Grade: {grade}
Subject: {subject}

Student Overview:
The student shows a developing understanding of the current curriculum.
Some foundational concepts are in place, but deeper comprehension is still forming.

Identified Weak Knowledge Areas:
- {chr(10).join(weak_points)}

Teaching Suggestions:
- Provide structured guidance when solving word problems
- Encourage step-by-step reasoning before calculations
- Reinforce conceptual understanding rather than memorization

Note:
This is a mock AI-generated analysis for demonstration purposes only.
Teachers should use this as a reference, not a final judgment.
"""

    return analysis_result


def main():
    base_dir = Path(__file__).resolve().parent.parent

    student_data_path = base_dir / "examples" / "sample_student_data.json"
    prompt_path = base_dir / "ai" / "prompt_templates" / "student_analysis_prompt.txt"

    student_data = load_json(student_data_path)
    prompt_template = load_prompt(prompt_path)

    print("Prompt template loaded successfully.")
    print("Student data loaded successfully.\n")

    analysis_output = mock_ai_analysis(student_data, prompt_template)

    print("===== AI ANALYSIS OUTPUT =====")
    print(analysis_output)


if __name__ == "__main__":
    main()

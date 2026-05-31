"""
Learning analysis service for EduInsight-AI.

This module contains the core business logic for analyzing student data
and generating learning reports.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .llm_adapter import LLMAdapter, MockLLMAdapter
from .models import (
    AnalysisResponse,
    KnowledgePoint,
    MasteryLevel,
    StudentData,
)


class LearningAnalysisService:
    """Service for generating learning analysis reports."""

    def __init__(
        self,
        llm_adapter: Optional[LLMAdapter] = None,
        prompt_template_path: Optional[str] = None,
    ):
        """
        Initialize the analysis service.

        Args:
            llm_adapter: LLM adapter to use for generating analysis.
                        If None, uses MockLLMAdapter.
            prompt_template_path: Path to custom prompt template.
        """
        self.llm_adapter = llm_adapter or MockLLMAdapter()
        self.prompt_template_path = prompt_template_path
        self._default_prompt_template = None

    def _load_prompt_template(self) -> str:
        """Load the prompt template from file or use default."""
        if self.prompt_template_path:
            path = Path(self.prompt_template_path)
            if path.exists():
                return path.read_text(encoding="utf-8")

        # Use embedded default template
        if self._default_prompt_template is None:
            default_path = (
                Path(__file__).parent.parent
                / "ai"
                / "prompt_templates"
                / "student_analysis_prompt.txt"
            )
            if default_path.exists():
                self._default_prompt_template = default_path.read_text(
                    encoding="utf-8"
                )
            else:
                self._default_prompt_template = self._get_fallback_prompt()

        return self._default_prompt_template

    def _get_fallback_prompt(self) -> str:
        """Fallback prompt template if file is not found."""
        return """You are an experienced K-12 education expert and instructional coach.

Your task is to analyze a student's learning data and generate a clear,
professional, and actionable learning analysis report for teachers.

IMPORTANT PRINCIPLES:
- This analysis is for instructional support only.
- Do NOT assign grades, labels, or rankings to the student.
- Do NOT make psychological or personal judgments.
- Focus on observable learning behaviors and academic evidence.
- Use encouraging, neutral, and professional language.

Please analyze the following student data and provide:
1. Student Overview
2. Academic Performance Analysis
3. Knowledge Point Analysis (weak and stable areas)
4. Common Learning Issues
5. Learning Behavior Insights
6. One-on-One Teaching Suggestions (3-5 specific strategies)
7. Personalized Study Suggestions for the student
8. AI Usage Disclaimer

Student Data:
{student_data}

Generate the learning analysis report now."""

    def _prepare_student_data_json(self, student_data: StudentData) -> str:
        """Convert student data to JSON string for the prompt."""
        return json.dumps(
            student_data.model_dump(mode="json"), indent=2, ensure_ascii=False
        )

    def _parse_llm_response(self, response_text: str, student_data: StudentData) -> Dict:
        """
        Parse the LLM response into structured sections.

        This is a simple parser that extracts sections based on markdown headers.
        For production use, you might want more sophisticated parsing.
        """
        lines = response_text.split("\n")

        sections = {
            "overview": "",
            "academic_performance": "",
            "knowledge_analysis": "",
            "common_issues": "",
            "behavior_insights": "",
            "teaching_suggestions": [],
            "study_suggestions": [],
            "disclaimer": "",
        }

        current_section = None
        current_content = []

        for line in lines:
            stripped = line.strip()

            # Detect section headers
            if stripped.startswith("##"):
                # Save previous section
                if current_section and current_content:
                    content = "\n".join(current_content).strip()
                    if current_section == "teaching_suggestions":
                        sections[current_section] = self._extract_numbered_items(content)
                    elif current_section == "study_suggestions":
                        sections[current_section] = self._extract_numbered_items(content)
                    else:
                        sections[current_section] = content
                    current_content = []

                # Determine new section
                header_lower = stripped.lower()
                if "overview" in header_lower:
                    current_section = "overview"
                elif "performance" in header_lower:
                    current_section = "academic_performance"
                elif "knowledge" in header_lower:
                    current_section = "knowledge_analysis"
                elif "issue" in header_lower or "mistake" in header_lower:
                    current_section = "common_issues"
                elif "behavior" in header_lower:
                    current_section = "behavior_insights"
                elif "teaching" in header_lower or "suggestion" in header_lower:
                    current_section = "teaching_suggestions"
                elif "study" in header_lower:
                    current_section = "study_suggestions"
                elif "disclaimer" in header_lower or "note" in header_lower:
                    current_section = "disclaimer"
                else:
                    current_section = None

            elif current_section and stripped:
                current_content.append(line)

        # Handle any remaining content
        if current_section and current_content:
            content = "\n".join(current_content).strip()
            if current_section in ["teaching_suggestions", "study_suggestions"]:
                sections[current_section] = self._extract_numbered_items(content)
            else:
                sections[current_section] = content

        # Fallback: if parsing failed, use the full response
        if not any(sections.values()):
            sections["overview"] = response_text

        return sections

    def _extract_numbered_items(self, text: str) -> List[str]:
        """Extract numbered or bulleted items from text."""
        items = []
        for line in text.split("\n"):
            stripped = line.strip()
            # Match numbered (1. 2. 3.) or bulleted (- *) items
            if stripped and (
                stripped[0].isdigit()
                or stripped.startswith("-")
                or stripped.startswith("*")
            ):
                # Remove the number/bullet and clean up
                item = stripped.lstrip("0123456789.-* ").strip()
                if item:
                    items.append(item)
        return items if items else [text]

    async def analyze_student(
        self, student_data: StudentData, custom_prompt: Optional[str] = None
    ) -> AnalysisResponse:
        """
        Generate a learning analysis report for a student.

        Args:
            student_data: The student's learning data
            custom_prompt: Optional custom prompt template

        Returns:
            AnalysisResponse containing the structured analysis
        """
        # Prepare the prompt
        prompt_template = custom_prompt or self._load_prompt_template()
        student_data_json = self._prepare_student_data_json(student_data)

        # Format the prompt with student data
        if "{student_data}" in prompt_template:
            prompt = prompt_template.format(student_data=student_data_json)
        else:
            prompt = f"{prompt_template}\n\nStudent Data:\n{student_data_json}"

        # System message for the LLM
        system_message = (
            "You are an experienced K-12 education expert and instructional coach. "
            "Generate professional, actionable, and encouraging learning analysis reports."
        )

        # Generate analysis using LLM
        llm_response = await self.llm_adapter.generate_completion(
            prompt=prompt, system_message=system_message
        )

        # Parse the response
        parsed_sections = self._parse_llm_response(llm_response, student_data)

        # Build the full formatted report
        full_report = self._format_full_report(
            student_data=student_data, sections=parsed_sections
        )

        # Create the response object
        return AnalysisResponse(
            student_id=student_data.student_profile.student_id,
            subject=student_data.subject.name,
            grade=student_data.student_profile.grade,
            overview=parsed_sections.get(
                "overview", "No overview generated."
            ),
            academic_performance_summary=parsed_sections.get(
                "academic_performance", "No performance analysis generated."
            ),
            knowledge_analysis=parsed_sections.get(
                "knowledge_analysis", "No knowledge analysis generated."
            ),
            common_issues=parsed_sections.get(
                "common_issues", "No common issues identified."
            ),
            behavior_insights=parsed_sections.get(
                "behavior_insights", "No behavior insights generated."
            ),
            teaching_suggestions=parsed_sections.get(
                "teaching_suggestions",
                [
                    "Provide structured guidance",
                    "Encourage step-by-step reasoning",
                    "Reinforce conceptual understanding",
                ],
            ),
            study_suggestions=parsed_sections.get(
                "study_suggestions",
                [
                    "Practice breaking problems into smaller steps",
                    "Review mistakes regularly",
                    "Focus on understanding over memorization",
                ],
            ),
            disclaimer=parsed_sections.get(
                "disclaimer",
                "This analysis is AI-generated for instructional support only. "
                "Final teaching decisions should be made by teachers based on professional judgment.",
            ),
            full_report=full_report,
            generated_at=datetime.utcnow().isoformat() + "Z",
        )

    def _format_full_report(
        self, student_data: StudentData, sections: Dict
    ) -> str:
        """Format the complete analysis report as markdown."""
        report = f"""# AI Learning Analysis Report

## Student Information
- **Student ID:** {student_data.student_profile.student_id}
- **Grade:** {student_data.student_profile.grade}
- **Subject:** {student_data.subject.name}
- **Semester:** {student_data.student_profile.semester}

---

## Student Overview

{sections.get('overview', 'Not available')}

---

## Academic Performance Summary

{sections.get('academic_performance', 'Not available')}

---

## Knowledge Point Analysis

{sections.get('knowledge_analysis', 'Not available')}

---

## Common Learning Issues

{sections.get('common_issues', 'Not available')}

---

## Learning Behavior Insights

{sections.get('behavior_insights', 'Not available')}

---

## Teaching Suggestions

{self._format_list(sections.get('teaching_suggestions', []))}

---

## Study Suggestions for Student

{self._format_list(sections.get('study_suggestions', []))}

---

## Important Note

{sections.get('disclaimer', 'This analysis is AI-generated for instructional support only.')}

---

*Generated by EduInsight-AI on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
        return report

    def _format_list(self, items: List[str]) -> str:
        """Format a list of items as markdown."""
        if not items:
            return "No suggestions available."
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def identify_weak_knowledge_points(
        self, student_data: StudentData
    ) -> List[KnowledgePoint]:
        """
        Identify knowledge points that need improvement.

        Args:
            student_data: The student's learning data

        Returns:
            List of knowledge points with weak or basic mastery
        """
        weak_levels = {MasteryLevel.weak, MasteryLevel.basic}
        return [
            kp
            for kp in student_data.knowledge_mastery
            if kp.mastery_level in weak_levels
        ]

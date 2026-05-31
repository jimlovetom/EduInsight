"""
Data models for EduInsight-AI.

This module defines Pydantic models for student data, analysis requests,
and analysis responses.
"""

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MasteryLevel(str, Enum):
    """Knowledge mastery levels."""

    weak = "weak"
    basic = "basic"
    average = "average"
    good = "good"
    excellent = "excellent"


class AssessmentType(str, Enum):
    """Types of assessments."""

    quiz = "quiz"
    homework = "homework"
    unit_test = "unit_test"
    midterm = "midterm"
    final = "final"
    other = "other"


class StudentProfile(BaseModel):
    """Student profile information (anonymized)."""

    student_id: str = Field(..., description="Anonymous student identifier")
    grade: str = Field(..., description="Grade level")
    semester: str = Field(..., description="Academic semester")
    learning_stage: str = Field(..., description="Educational stage")
    notes: Optional[str] = Field(None, description="Additional notes")


class SubjectInfo(BaseModel):
    """Subject and curriculum information."""

    name: str = Field(..., description="Subject name")
    curriculum_standard: str = Field(..., description="Curriculum standard")
    current_topics: List[str] = Field(..., description="Current learning topics")


class AssessmentScore(BaseModel):
    """Individual assessment score."""

    assessment_type: AssessmentType = Field(..., description="Type of assessment")
    topic: str = Field(..., description="Assessment topic")
    score_val: float = Field(..., description="Score obtained", alias="score")
    full_score: float = Field(..., description="Maximum possible score")
    assessment_date: date = Field(..., description="Assessment date", alias="date")


class AcademicPerformance(BaseModel):
    """Overall academic performance data."""

    recent_scores: List[AssessmentScore] = Field(
        ..., description="Recent assessment scores"
    )
    overall_trend: str = Field(..., description="Performance trend description")


class KnowledgePoint(BaseModel):
    """Knowledge point mastery information."""

    knowledge_point: str = Field(..., description="Name of knowledge point")
    mastery_level: MasteryLevel = Field(..., description="Mastery level")
    evidence: str = Field(..., description="Evidence for mastery assessment")


class CommonMistake(BaseModel):
    """Common mistake pattern."""

    mistake_type: str = Field(..., description="Type of mistake")
    description: str = Field(..., description="Description of the mistake")
    frequency: str = Field(..., description="Frequency of occurrence")


class LearningBehavior(BaseModel):
    """Learning behavior patterns."""

    homework_completion: str = Field(..., description="Homework completion status")
    class_participation: str = Field(..., description="Class participation level")
    study_habits: List[str] = Field(..., description="Study habits")


class TeacherObservations(BaseModel):
    """Teacher's observations about the student."""

    strengths: List[str] = Field(..., description="Student strengths")
    weaknesses: List[str] = Field(..., description="Areas needing improvement")
    additional_comments: Optional[str] = Field(
        None, description="Additional comments"
    )


class StudentData(BaseModel):
    """Complete student data structure."""

    student_profile: StudentProfile = Field(..., description="Student profile")
    subject: SubjectInfo = Field(..., description="Subject information")
    academic_performance: AcademicPerformance = Field(
        ..., description="Academic performance"
    )
    knowledge_mastery: List[KnowledgePoint] = Field(
        ..., description="Knowledge mastery levels"
    )
    common_mistakes: List[CommonMistake] = Field(
        ..., description="Common mistakes"
    )
    learning_behavior: LearningBehavior = Field(..., description="Learning behavior")
    teacher_observations: TeacherObservations = Field(
        ..., description="Teacher observations"
    )


class AnalysisRequest(BaseModel):
    """Request for learning analysis."""

    student_data: StudentData = Field(..., description="Student data to analyze")
    prompt_template: Optional[str] = Field(
        None, description="Custom prompt template (optional)"
    )


class AnalysisSection(BaseModel):
    """A section in the analysis report."""

    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")


class AnalysisResponse(BaseModel):
    """Response containing the learning analysis."""

    student_id: str = Field(..., description="Student identifier")
    subject: str = Field(..., description="Subject name")
    grade: str = Field(..., description="Grade level")
    overview: str = Field(..., description="Student overview")
    academic_performance_summary: str = Field(
        ..., description="Academic performance summary"
    )
    knowledge_analysis: str = Field(..., description="Knowledge point analysis")
    common_issues: str = Field(..., description="Common learning issues")
    behavior_insights: str = Field(..., description="Learning behavior insights")
    teaching_suggestions: List[str] = Field(
        ..., description="Teaching suggestions for teachers"
    )
    study_suggestions: List[str] = Field(
        ..., description="Study suggestions for students"
    )
    disclaimer: str = Field(..., description="AI usage disclaimer")
    full_report: str = Field(..., description="Complete formatted report")
    generated_at: str = Field(..., description="Report generation timestamp")

"""
Tests for EduInsight-AI backend.

This module contains unit tests for the backend components.
"""

import json
from pathlib import Path

import pytest

from backend.models import (
    AcademicPerformance,
    AssessmentScore,
    AssessmentType,
    CommonMistake,
    KnowledgePoint,
    LearningBehavior,
    MasteryLevel,
    StudentData,
    StudentProfile,
    SubjectInfo,
    TeacherObservations,
)


@pytest.fixture
def sample_student_data():
    """Fixture providing sample student data."""
    return {
        "student_profile": {
            "student_id": "TEST_001",
            "grade": "Grade 7",
            "semester": "2024 Spring",
            "learning_stage": "middle_school",
        },
        "subject": {
            "name": "Mathematics",
            "curriculum_standard": "National Curriculum",
            "current_topics": ["Linear equations", "Word problems"],
        },
        "academic_performance": {
            "recent_scores": [
                {
                    "assessment_type": "quiz",
                    "topic": "Linear equations",
                    "score": 75.0,
                    "full_score": 100.0,
                    "date": "2024-03-15",
                }
            ],
            "overall_trend": "stable",
        },
        "knowledge_mastery": [
            {
                "knowledge_point": "Solving linear equations",
                "mastery_level": "basic",
                "evidence": "Some calculation errors",
            }
        ],
        "common_mistakes": [
            {
                "mistake_type": "calculation_error",
                "description": "Sign errors",
                "frequency": "medium",
            }
        ],
        "learning_behavior": {
            "homework_completion": "on_time",
            "class_participation": "moderate",
            "study_habits": ["Reviews notes regularly"],
        },
        "teacher_observations": {
            "strengths": ["Good effort"],
            "weaknesses": ["Needs more practice"],
            "additional_comments": "Making progress",
        },
    }


class TestModels:
    """Test Pydantic models."""

    def test_student_profile_creation(self):
        """Test creating a StudentProfile."""
        profile = StudentProfile(
            student_id="TEST_001",
            grade="Grade 7",
            semester="2024 Spring",
            learning_stage="middle_school",
        )
        assert profile.student_id == "TEST_001"
        assert profile.grade == "Grade 7"

    def test_knowledge_point_creation(self):
        """Test creating a KnowledgePoint."""
        kp = KnowledgePoint(
            knowledge_point="Linear equations",
            mastery_level=MasteryLevel.basic,
            evidence="Student shows basic understanding",
        )
        assert kp.knowledge_point == "Linear equations"
        assert kp.mastery_level == MasteryLevel.basic

    def test_mastery_level_enum(self):
        """Test MasteryLevel enum values."""
        assert MasteryLevel.weak.value == "weak"
        assert MasteryLevel.basic.value == "basic"
        assert MasteryLevel.average.value == "average"
        assert MasteryLevel.good.value == "good"
        assert MasteryLevel.excellent.value == "excellent"

    def test_assessment_type_enum(self):
        """Test AssessmentType enum values."""
        assert AssessmentType.quiz.value == "quiz"
        assert AssessmentType.homework.value == "homework"
        assert AssessmentType.unit_test.value == "unit_test"

    def test_full_student_data_creation(self, sample_student_data):
        """Test creating complete StudentData object."""
        student_data = StudentData(**sample_student_data)
        assert student_data.student_profile.student_id == "TEST_001"
        assert student_data.subject.name == "Mathematics"
        assert len(student_data.knowledge_mastery) == 1


class TestLLMAdapter:
    """Test LLM adapters."""

    @pytest.mark.asyncio
    async def test_mock_llm_adapter(self):
        """Test MockLLMAdapter generates response."""
        from backend.llm_adapter import MockLLMAdapter

        adapter = MockLLMAdapter()
        response = await adapter.generate_completion(
            prompt="Test prompt",
            system_message="Test system message",
        )
        assert response is not None
        assert len(response) > 0
        assert adapter.get_model_name() == "mock-llm-v1"

    def test_create_llm_adapter_factory(self):
        """Test LLM adapter factory function."""
        from backend.llm_adapter import create_llm_adapter, MockLLMAdapter

        # Test mock adapter creation
        adapter = create_llm_adapter("mock")
        assert isinstance(adapter, MockLLMAdapter)

        # Test invalid provider
        with pytest.raises(ValueError):
            create_llm_adapter("invalid_provider")


class TestAnalysisService:
    """Test LearningAnalysisService."""

    @pytest.mark.asyncio
    async def test_identify_weak_knowledge_points(self, sample_student_data):
        """Test identifying weak knowledge points."""
        from backend.analysis_service import LearningAnalysisService
        from backend.models import StudentData

        student_data = StudentData(**sample_student_data)
        service = LearningAnalysisService()

        weak_points = service.identify_weak_knowledge_points(student_data)
        assert len(weak_points) == 1
        assert weak_points[0].knowledge_point == "Solving linear equations"

    @pytest.mark.asyncio
    async def test_analyze_student(self, sample_student_data):
        """Test full student analysis."""
        from backend.analysis_service import LearningAnalysisService
        from backend.models import StudentData

        student_data = StudentData(**sample_student_data)
        service = LearningAnalysisService()

        result = await service.analyze_student(student_data)

        assert result.student_id == "TEST_001"
        assert result.subject == "Mathematics"
        assert result.grade == "Grade 7"
        assert result.full_report is not None
        assert len(result.teaching_suggestions) > 0
        assert len(result.study_suggestions) > 0


class TestDataLoading:
    """Test data loading functionality."""

    def test_load_sample_student_data(self):
        """Test loading sample student data from file."""
        base_dir = Path(__file__).parent.parent
        sample_path = base_dir / "examples" / "sample_student_data.json"

        assert sample_path.exists()

        with open(sample_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate it can be parsed as StudentData
        student_data = StudentData(**data)
        assert student_data.student_profile.student_id == "SAMPLE_001"

    def test_load_prompt_template(self):
        """Test loading prompt template from file."""
        base_dir = Path(__file__).parent.parent
        prompt_path = (
            base_dir / "ai" / "prompt_templates" / "student_analysis_prompt.txt"
        )

        assert prompt_path.exists()

        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()

        assert len(template) > 0
        assert "K-12" in template or "education" in template.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

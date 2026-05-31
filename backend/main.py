"""
FastAPI application for EduInsight-AI.

This module provides the REST API endpoints for the learning analysis service.
"""

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from .analysis_service import LearningAnalysisService
from .llm_adapter import create_llm_adapter
from .models import AnalysisRequest, AnalysisResponse, StudentData

# Create FastAPI app
app = FastAPI(
    title="EduInsight-AI API",
    description="AI-powered learning analysis tool for K-12 education",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the analysis service
analysis_service = LearningAnalysisService()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic information."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EduInsight-AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #2c3e50; }
            .info { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
            a { color: #3498db; }
        </style>
    </head>
    <body>
        <h1>🎓 EduInsight-AI API</h1>
        <div class="info">
            <p><strong>EduInsight-AI</strong> is an AI-powered learning analysis tool designed for K-12 teachers.</p>
            <p>It helps educators better understand student learning progress and provide effective one-on-one instructional support.</p>
        </div>
        <h2>API Documentation</h2>
        <ul>
            <li><a href="/docs">Swagger UI Documentation</a></li>
            <li><a href="/redoc">ReDoc Documentation</a></li>
        </ul>
        <h2>Available Endpoints</h2>
        <ul>
            <li><code>GET /</code> - This welcome page</li>
            <li><code>GET /health</code> - Health check endpoint</li>
            <li><code>POST /api/v1/analyze</code> - Generate learning analysis</li>
            <li><code>POST /api/v1/analyze/upload</code> - Upload student data file</li>
        </ul>
        <h2>Features</h2>
        <ul>
            <li>📊 Student learning profile analysis</li>
            <li>🧠 Knowledge gap identification</li>
            <li>🎯 One-on-one teaching suggestions</li>
            <li>🧩 Explainable AI results</li>
            <li>🔒 Student data anonymization support</li>
        </ul>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "EduInsight-AI",
        "version": "0.1.0",
    }


@app.post(
    "/api/v1/analyze",
    response_model=AnalysisResponse,
    summary="Generate Learning Analysis",
    description="Analyze student learning data and generate an AI-powered report.",
)
async def analyze_student(request: AnalysisRequest):
    """
    Generate a learning analysis report for a student.

    This endpoint accepts student learning data and returns a comprehensive
    AI-generated analysis including:
    - Student overview
    - Academic performance summary
    - Knowledge point analysis
    - Common learning issues
    - Learning behavior insights
    - Teaching suggestions for educators
    - Study suggestions for students

    **Important:** This analysis is for instructional support only and should
    not be used as the sole basis for student evaluation or grading.
    """
    try:
        # Use custom prompt if provided
        if request.prompt_template:
            service = LearningAnalysisService()
        else:
            service = analysis_service

        # Generate analysis
        result = await service.analyze_student(
            student_data=request.student_data,
            custom_prompt=request.prompt_template,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@app.post(
    "/api/v1/analyze/upload",
    response_model=AnalysisResponse,
    summary="Analyze from Uploaded File",
    description="Upload a JSON file containing student data for analysis.",
)
async def analyze_from_file(
    file_content: str,
    prompt_template: Optional[str] = None,
):
    """
    Analyze student data from an uploaded JSON file.

    The file should contain student data in the expected JSON format.
    See the sample_student_data.json in the examples directory for reference.
    """
    try:
        # Parse the JSON content
        data = json.loads(file_content)

        # Validate using Pydantic model
        student_data = StudentData(**data)

        # Generate analysis
        service = LearningAnalysisService()
        result = await service.analyze_student(
            student_data=student_data,
            custom_prompt=prompt_template,
        )

        return result

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON format: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid student data: {str(e)}",
        )


@app.get(
    "/api/v1/sample-data",
    response_model=StudentData,
    summary="Get Sample Student Data",
    description="Retrieve sample student data for testing purposes.",
)
async def get_sample_data():
    """
    Get sample student data for testing the API.

    This returns the sample data from examples/sample_student_data.json
    """
    try:
        base_dir = Path(__file__).parent.parent
        sample_path = base_dir / "examples" / "sample_student_data.json"

        if not sample_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sample data file not found",
            )

        with open(sample_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return StudentData(**data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load sample data: {str(e)}",
        )


@app.get(
    "/api/v1/prompt-template",
    summary="Get Prompt Template",
    description="Retrieve the default prompt template used for analysis.",
)
async def get_prompt_template():
    """
    Get the default prompt template used for learning analysis.
    """
    try:
        base_dir = Path(__file__).parent.parent
        prompt_path = (
            base_dir / "ai" / "prompt_templates" / "student_analysis_prompt.txt"
        )

        if not prompt_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prompt template file not found",
            )

        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()

        return {"template": template}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load prompt template: {str(e)}",
        )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested resource was not found.",
            "help": "Please check the API documentation at /docs",
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred.",
            "help": "Please try again later or contact support.",
        },
    )

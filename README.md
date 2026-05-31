# EduInsight-AI

EduInsight-AI is an AI-powered learning analysis tool designed for K-12 teachers.
It helps educators better understand student learning progress and provide effective one-on-one instructional support.

---

## 🎯 Project Vision

Teachers often face challenges in analyzing individual student learning situations due to limited time and scattered data.
EduInsight-AI leverages large language model (LLM) APIs to transform student learning data into actionable insights,
supporting personalized teaching and targeted learning improvement.

---

## ✨ Key Features

- 📊 **Student Learning Profile Analysis** - Comprehensive analysis of student academic performance
- 🧠 **Knowledge Gap Identification** - Automatically identify weak knowledge areas
- 🎯 **One-on-One Teaching Suggestions** - Personalized instructional strategies for teachers
- 🧩 **Explainable AI Results** - Clear reasoning and evidence for all analysis
- 🔒 **Student Data Anonymization** - Privacy-focused design with anonymized data handling
- 🔌 **Pluggable LLM Adapters** - Support for multiple LLM providers (OpenAI, Azure, Mock)

---

## 👩‍🏫 Target Users

- Primary and secondary school teachers
- Head teachers and subject teachers
- Education researchers and developers

---

## 🏗️ Architecture

### Backend Stack

- **Framework**: FastAPI (Python)
- **Data Validation**: Pydantic
- **LLM Integration**: Pluggable adapter pattern
- **Supported LLM Providers**:
  - Mock (for testing/demo)
  - OpenAI API
  - Azure OpenAI Service

### Project Structure

```
eduinsight-ai/
├── ai/
│   └── prompt_templates/
│       └── student_analysis_prompt.txt
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic data models
│   ├── analysis_service.py  # Core analysis logic
│   ├── llm_adapter.py       # LLM provider adapters
│   ├── config.py            # Configuration settings
│   ├── demo_analysis.py     # Demo script
│   └── tests/
│       ├── __init__.py
│       └── test_backend.py
├── examples/
│   ├── sample_student_data.json
│   └── sample_analysis_output.md
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eduinsight-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional)**
   
   Create a `.env` file for configuration:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` to set your LLM provider credentials if needed.

### Running the Demo

Run the demo analysis script:
```bash
python backend/demo_analysis.py
```

### Starting the API Server

Start the FastAPI server:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📖 API Usage

### Generate Learning Analysis

**Endpoint**: `POST /api/v1/analyze`

**Request Body**:
```json
{
  "student_data": {
    "student_profile": {
      "student_id": "STU_001",
      "grade": "Grade 7",
      "semester": "2024 Spring",
      "learning_stage": "middle_school"
    },
    "subject": {
      "name": "Mathematics",
      "curriculum_standard": "National Curriculum",
      "current_topics": ["Linear equations", "Word problems"]
    },
    "academic_performance": {
      "recent_scores": [...],
      "overall_trend": "stable"
    },
    "knowledge_mastery": [...],
    "common_mistakes": [...],
    "learning_behavior": {...},
    "teacher_observations": {...}
  }
}
```

**Response**: Structured analysis report with sections for overview, performance, knowledge gaps, and suggestions.

### Get Sample Data

**Endpoint**: `GET /api/v1/sample-data`

Returns sample student data for testing purposes.

### Upload File for Analysis

**Endpoint**: `POST /api/v1/analyze/upload`

Upload a JSON file containing student data for analysis.

---

## 📝 Data Format

### Student Data Schema

The student data JSON should include:

- **student_profile**: Anonymous student information
- **subject**: Subject and curriculum details
- **academic_performance**: Assessment scores and trends
- **knowledge_mastery**: Knowledge point mastery levels
- **common_mistakes**: Frequent error patterns
- **learning_behavior**: Study habits and participation
- **teacher_observations**: Teacher's notes on strengths/weaknesses

See `examples/sample_student_data.json` for a complete example.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | EduInsight-AI |
| `DEBUG` | Debug mode | false |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `LLM_PROVIDER` | LLM provider (mock/openai/azure) | mock |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model | gpt-3.5-turbo |
| `AZURE_API_KEY` | Azure API key | - |
| `AZURE_ENDPOINT` | Azure endpoint | - |
| `AZURE_MODEL` | Azure model | gpt-35-turbo |

---

## 🧪 Testing

Run the test suite:

```bash
pytest backend/tests/ -v
```

---

## ⚠️ Ethics & Disclaimer

This project is intended **only as an instructional support tool**.

- AI-generated analysis and suggestions should **not** be used as the sole basis for student evaluation, grading, or academic decisions.
- Teachers always retain full decision-making authority.
- The system is designed to support, not replace, professional educator judgment.
- Student data should be anonymized before processing.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For questions or issues, please open an issue in the repository.

---

*EduInsight-AI - Empowering teachers with AI-driven insights*

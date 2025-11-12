# Automotive Code Security Scanner

A static security analysis tool designed specifically for automotive software development, focusing on identifying vulnerabilities in C++ codebases used in vehicle systems.

## Overview

This application leverages AI-powered analysis to scan C++ code for common security vulnerabilities based on automotive industry standards and best practices. The system uses a RAG (Retrieval-Augmented Generation) model trained on comprehensive documentation of C++ vulnerabilities to provide detailed security assessments.

## Features

- **Automated Security Scanning**: Upload C++ files for immediate vulnerability analysis
- **AI-Powered Detection**: Utilizes OpenAI GPT-4o Mini with RAG architecture for intelligent pattern recognition
- **Automotive-Focused**: Trained on C++ vulnerabilities commonly found in automotive software
- **Detailed Reports**: Generates comprehensive JSON reports with vulnerability details
- **Cloud Storage**: Secure file storage and report archival using AWS S3
- **Modern Web Interface**: Responsive React frontend for easy file uploads and report viewing

## Architecture

### Backend
- **Framework**: FastAPI (Python)
- **AI/ML Stack**: 
  - LangChain for LLM orchestration
  - OpenAI GPT-4o Mini for code analysis
  - ChromaDB for vector storage and retrieval
- **Cloud Storage**: AWS S3 via Boto3
- **Processing Flow**:
  1. User uploads C++ file via API
  2. File stored in S3 bucket
  3. RAG model retrieves relevant vulnerability patterns from vector database
  4. AI analyzes code against known vulnerabilities
  5. Results returned as JSON and stored in S3

### Frontend
- **Framework**: React + Vite
- **Purpose**: File upload interface and vulnerability report display

## Prerequisites

- Python 3.8 - 3.11, python 3.12+ will not work
- Node.js 16+
- AWS Account with S3 access
- OpenAI API key

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/vibhas-krishnapuram/MLVehicleSecScanner.git
cd MLVehicleScanner
```

2. Install Python dependencies inside venv:
```bash
python3.11 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export AWS_ACCESS_KEY="your-aws-access-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
export AWS_REGION = "your-bucket-region"
export S3_BUCKET_NAME="your-s3-bucket-name"
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Starting the Backend

```bash
uvicorn main_CloudStorage:app --reload
```

The API will be available at `http://localhost:8000`

### Starting the Frontend

```bash
cd frontend
npm run dev
```


### API Endpoints

- `POST /upload` - Upload C++ file for analysis
- `GET /files/{file_name}` - See uploaded files
- `GET /response/{report_name}` - See JSON response of vulnerabilites found

## Key Dependencies

### Backend
- `fastapi` - Web framework
- `langchain` - LLM orchestration
- `chromadb` - Vector database
- `boto3` - AWS S3 integration
- `openai` - GPT-4o Mini integration

### Frontend
- `react` - UI framework
- `vite` - Build tool and dev server

## How It Works

1. **Upload**: User uploads a C++ source file through the web interface
2. **Storage**: File is securely stored in AWS S3
3. **Retrieval**: RAG model queries ChromaDB for relevant vulnerability patterns
4. **Analysis**: OpenAI GPT-4o Mini analyzes the code using retrieved context
5. **Report Generation**: Vulnerabilities are compiled into a JSON report
6. **Storage & Response**: Report is saved to S3 and returned to the user

## Security Considerations

- All uploaded files are stored securely in AWS S3
- API keys should never be committed to version control
- Use IAM roles with minimal required permissions for AWS access
- Consider implementing rate limiting for production deployments

## Contributing

Contributions are welcome! Please follow these guidelines:
- Follow PEP 8 style guide for Python code
- Use ESLint configuration for JavaScript/React code
- Add tests for new features
- Update documentation as needed


## Roadmap

- [ ] Support for additional languages (C, Rust)
- [ ] Integration with CI/CD pipelines
- [ ] Custom vulnerability pattern training
- [ ] Enhanced reporting with remediation suggestions
- [ ] Multi-file project scanning

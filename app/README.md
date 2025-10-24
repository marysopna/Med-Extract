
---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/marysopna/Med-Extract.git
cd app

## 2. Create a virtual environment
python -m venv venv
source venv/bin/activate

## 3. Install the required packages
pip install -r requirements.txt

## 4. Add your .env file in root directory
OPENAI_API_KEY=your_openai_key_here

## Run the Fastapi solution
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

## Curl command to test API Endpoints
curl -X POST http://localhost:8080/documents/upload   -F "file=pdf or text file name"
curl -X POST http://localhost:8080/query/ask   -H "Content-Type: application/json"   -d '{"question": "your question here"}'


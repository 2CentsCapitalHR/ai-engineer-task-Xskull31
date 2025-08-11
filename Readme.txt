# Corporate Document Compliance Agent (ADGM Regulations)

## 📌 Overview
This project is an AI-powered **corporate compliance assistant** that automatically checks legal and corporate documents against **Abu Dhabi Global Market (ADGM) regulations**.

It uses:
- **RAG** (Retrieval-Augmented Generation) for finding exact clauses from official ADGM regulations.
- **LLM** (Large Language Model) for legal compliance checks and improvement suggestions.
- **Rule-based checks** for fast, explainable detection of common compliance issues.

---------------------------------------------------------

## ⚙️ Features
✅ **Document-type detection** (e.g., Company Incorporation, Employment & HR, Commercial Agreements)  
✅ **Checklist verification** – detects missing required documents for a process  
✅ **Red-flag detection** – catches jurisdiction mismatches, missing clauses, missing signatures  
✅ **RAG-powered LLM checks** – verifies clauses against ADGM regulations with citations  
✅ **Inline review comments** – inserts `[REVIEW]` notes in `.docx` output  
✅ **Multiple LLM backends** supported – **Ollama** (local), OpenAI, Gemini, Claude  

--------------------------------------------------------------

## 📂 Folder Structure
corporate-agent/
│
├── app.py # Main application entry point
├── .env # Environment variables (API keys, model choice)
│
├── rag/ # RAG (Retrieval-Augmented Generation) pipeline
│ ├── indexer.py # Creates vector index from ADGM docs
│ ├── retriever.py # Retrieves top matching regulation passages
│ ├── test_compliance.py # Test script for compliance checks
│ ├── index/ # FAISS index storage
│ └── raw/ # Original raw documents for indexing
│
├── utils/ # Helper functions
│ ├── text_extractor.py # Extracts text from PDF/DOCX
│ ├── docx_writer.py # Adds review comments to DOCX
│ └── llm_client.py # LLM integration (Ollama, OpenAI, etc.)
│
├── Pipeline
| ├── checklist.py # Required-documents check
│ ├── flags.py # Rule-based red flag detection
└── requirements.txt # Python dependencies

----------------------------------------------------------
Create virtual environment
	python -m venv venv

Windows (PowerShell)
	venv\Scripts\Activate.ps1

Use Ollama (Local)
	Install Ollama:
	 https://ollama.ai/download

	Pull a model:
	 ollama pull mistral
	
	In .env, set:
	 LLM_BACKEND=ollama
 	 OLLAMA_MODEL=mistral
-----------------------------------------------------------

📑 Example Workflow
Place ADGM regulation documents in rag/raw/ and run:
Upload a .docx legal document through the app.

The app:
Detects document type
Runs checklist verification
Runs rule-based red flag detection
Retrieves matching ADGM regulation passages
Runs LLM compliance check
Generates .docx with review comments
Output saved to output/ folder.
------------------------------------------------------------


🧪 Testing with Sample Document
A ready-made sample is provided:
📄 sample_complex_test.docx

Use it to test:
python app.py

Upload this file and review the generated .docx output.
-------------------------------------------------------------

🔮 How RAG + LLM Works
Retrieve: FAISS searches ADGM regulation index for top relevant passages to your clause.

Augment: The retrieved passages are added to the LLM prompt.

Generate: The LLM decides compliance status, suggests edits, and cites regulation text.

-------------------------------------------------------------

Author
Developed by Prateek S Nyamagoudar  (prateeksn31@gmail.com)
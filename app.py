import os
import json
import tempfile
from pathlib import Path
from pipeline.ingest import read_docx
from pipeline.checklists import detect_document_types, REQUIRED_DOCS
from pipeline.flags import find_issues
from utils.docx_writer import append_review
import gradio as gr
from pipeline.checklists import detect_document_types, checklist_verification


def review_docx(file):
    """Main pipeline invoked by Gradio. Returns (reviewed_docx_path, report_dict)."""
    if not file:
        return None, {"error": "no file provided"}

    # gradio may pass a path string or a file-like object. Normalize to path.
    if isinstance(file, str):
        input_path = file
    else:
        # file is an UploadedFile-like object
        try:
            input_path = file.name
        except Exception:
            # fallback: write bytes to temp
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
            tmp.write(file.read())
            tmp.close()
            input_path = tmp.name

    # Create a working temp dir
    workdir = tempfile.mkdtemp(prefix="corp_agent_")
    saved_input = os.path.join(workdir, os.path.basename(input_path))
    Path(saved_input).write_bytes(Path(input_path).read_bytes())

    # Ingest
    paras, tables, full_text = read_docx(saved_input)

    # Detect documents / process
    detected_docs, inferred_process = detect_document_types(paras)
    required, missing = checklist_verification(detected_docs, inferred_process)

# Flags / issues
    issues = find_issues(full_text, paras)

    report = {
        "process": inferred_process,
        "documents_uploaded": len(detected_docs),
        "detected_documents": detected_docs,
        "required_documents": required,
        "missing_documents": missing,
        "issues_found": issues
    }
    # Checklist
    required = REQUIRED_DOCS.get(inferred_process, [])
    missing = list(set(required) - set(detected_docs))

    

    # Build report
    report = {
        "process": inferred_process,
        "documents_uploaded": len(detected_docs),
        "detected_documents": detected_docs,
        "required_documents": required,
        "missing_documents": missing,
        "issues_found": issues,
    }

    # Produce reviewed docx
    reviewed_path = os.path.join(workdir, "reviewed_" + os.path.basename(input_path))
    append_review(saved_input, issues, reviewed_path)

    # Save JSON report
    report_path = os.path.join(workdir, "report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return reviewed_path, report


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("# Corporate Agent — MVP Review Demo")
        with gr.Row():
            inp = gr.File(label="Upload .docx (single file)")
            run = gr.Button("Run Review")
        out_file = gr.File(label="Download reviewed .docx")
        out_json = gr.JSON(label="Report (JSON)")

        run.click(review_docx, inputs=inp, outputs=[out_file, out_json])

    demo.launch()
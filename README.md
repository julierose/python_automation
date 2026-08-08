# Business Automation Demos
 
A small collection of scripts demonstrating how to automate common business document workflows — generating branded PowerPoint decks, Word documents, and Excel reports from data, on demand.
 
Each subfolder is a self-contained, runnable example: a script, a branded template, sample output, and its own README with setup and customization notes.
 
## Demos
 
| Demo | Status | Description |
|---|---|---|
| [`pptx_automation/`](pptx_automation/) | Available | Automates branded PowerPoint deck generation — inserts a data-driven chart and a dynamic "last refreshed" text box into a template deck using python-pptx, pandas, and seaborn. |
| `docx_automation/` | Coming soon | Automated Word document generation |
| `email_report_automation/` | Coming soon | Generates a report with Quarto, then converts it to a PNG for embedding directly in email bodies — sidesteps HTML stripping/formatting issues in email platforms like Gmail. |
 
## Why this exists
 
These demos show a reusable pattern: take a branded template, populate it programmatically with current data, and produce a polished, ready-to-share document — without manual copy-pasting or reformatting. The same approach extends to recurring reports, client-facing decks, and other repetitive document work.
 
## Getting started
 
Each demo folder has its own `README.md` and `requirements.txt`. To run one:
 
```
cd pptx_automation
pip install -r requirements.txt
python generate_deck.py
```
 
## About
 
Built as a demonstration of business process automation skills. If you're interested in adapting any of these for your own workflows or templates, feel free to reach out.

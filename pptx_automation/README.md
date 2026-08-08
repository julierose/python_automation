# PowerPoint Automation Demo
 
A demonstration of automating branded PowerPoint deck creation using [python-pptx](https://python-pptx.readthedocs.io/), pandas, and seaborn/matplotlib. This script loads an existing branded template, embeds a chart built from sample data, and adds a dynamic "last refreshed" text box — a pattern well-suited for recurring reports, client dashboards, or any deck that needs to be regenerated on a schedule.
 
## What it does
 
1. Builds a sample dataset with pandas and creates a boxplot with seaborn.
2. Saves the chart to a temporary file (never committed to the repo).
3. Opens `Sample_Deck_Template.pptx` — a pre-branded PowerPoint template.
4. Inserts the chart into a content slide at a specified position and size.
5. Adds a text box to the title slide showing the date the deck was last generated.
6. Saves the result as `Sample_Deck_Updated.pptx`.
## Requirements
 
- Python 3.11 or higher
- Packages listed in `requirements.txt`
Install dependencies:
 
```
pip install -r requirements.txt
```
> **Note:** this project is built and tested on pandas 3.0.5, a recent major release (January 2026) that changed some default behaviors (e.g. copy-on-write is now on by default). If you already have an older version of pandas installed in a shared environment, running `pip install -r requirements.txt` will upgrade it — which could affect other projects relying on pre-3.0 behavior. Consider using a virtual environment to keep this isolated.

## Usage
 
From within this folder:
 
```
python generate_deck.py
```
 
(On Mac/Linux, you may need `python3` instead of `python`, depending on your setup.)
 
This will regenerate `Sample_Deck_Updated.pptx` in the same folder, using the current date for the "last refreshed" text.
 
## Template requirements
 
This script is written against a specific template structure. If you swap in your own `.pptx` template, make sure it has:
 
- At least 3 slides
- A title slide as slide 1 (index `0`) — this is where the "last refreshed" text box is added
- A content slide as slide 3 (index `2`) — this is where the chart is inserted
If your template has a different structure, adjust the slide index values (`prs.slides[...]`) in `generate_deck.py` accordingly.
 
## Customizing for your own use
 
This script is meant as a starting point. Common things to adjust:
 
- **Data**: replace the `test_data` dictionary with your own data source (CSV, Excel, database query, API call, etc.)
- **Chart type/styling**: swap the seaborn boxplot for any chart type, or adjust colors/fonts to match your brand
- **Chart position/size**: adjust `chart_left_position`, `chart_top_position`, and `chart_image_height`
- **Text box content, font, size, and color**: adjust the `run.font` properties near the bottom of the script
- **Template**: swap in your own branded `.pptx` file (see template requirements above)
## Files in this folder
 
| File | Purpose |
|---|---|
| `generate_deck.py` | Main script |
| `Sample_Deck_Template.pptx` | Input template |
| `Sample_Deck_Updated.pptx` | Example output (committed so you can see the result without running the script) |
| `requirements.txt` | Python package dependencies |
 
## About
 
Part of a small collection of business process automation demos — see the [repository root](../README.md) for other examples (Word, Excel, etc.).
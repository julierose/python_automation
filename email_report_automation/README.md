# Email Report Automation

Generates a branded, data-driven report with [Quarto](https://quarto.org/), then converts the rendered HTML into a cropped PNG image suitable for embedding directly in the body of an email.

## Why this exists

Quarto is excellent for producing polished, reusable HTML reports, but most major email clients (Gmail, Outlook, etc.) strip out embedded HTML/CSS, so a report that looks great as a standalone webpage often breaks or renders inconsistently when pasted into an email body. Converting the rendered report to a single image sidesteps that problem entirely: what you see is exactly what recipients see, regardless of their email client.

This workflow is especially useful for executive-facing reporting. Leadership teams often want a quick, at-a-glance snapshot of the latest organizational metrics without having to open an attachment, log into a dashboard, or click through to a separate site. A report that lands directly in the inbox, fully rendered and readable in seconds, removes that friction.

## What it does

1. **`email_report_automation.qmd`**: a Quarto report that reads in sample environmental metric data, renders a chart (including recent data, future projections, and progress towards a goal, with a bay-comparison inset for context) and a small summary table, all driven by dynamic values (report date, progress-to-goal percentage, etc.) rather than hardcoded text.
2. **`report_image_generation.py`**: a wrapper script that:
   - Renders the `.qmd` file to HTML via the Quarto CLI (`subprocess`)
   - Converts that HTML to a PNG screenshot using `html2image`
   - Auto-crops excess whitespace from the bottom of the image (via Pillow) so the final PNG fits tightly around the actual report content, ready to drop into an email body

## Sample data

This demo uses fully synthetic data (`environmental_report_sample_data.csv`, and `bay_comparison.csv`) standing in for a proprietary reporting pipeline. Swap in your own data source! A database query, API call, or internal CSV export will yield the same rendering and image-conversion logic applied unchanged.

## Getting started

This demo requires the [Quarto CLI](https://quarto.org/docs/get-started/) to be installed separately. It isn't a pip package, so `requirements.txt` alone won't cover it.

```
cd email_report_automation
pip install -r requirements.txt
python report_image_generation.py
```

This produces `email_report_automation.html` (the standalone rendered report) and `email_report.png` (the cropped image, ready to paste into an email body).

A pre-rendered example of both outputs is included in this folder for reference, see `email_report_automation.html` and `email_report.png`.

## Customizing

- **Data**: point the `.qmd` file's `pd.read_csv()` calls at your own data source.
- **Branding**: colors, fonts, and layout are controlled via the `<style>` block at the top of the `.qmd` file and inline in the matplotlib chart code. Update both to match your organization's branding.
- **Report cadence**: `report_date` is currently hardcoded for demonstration; in production, set it dynamically (e.g. `pd.Timestamp.today()`) and schedule `report_image_generation.py` to run on a recurring basis (cron, Task Scheduler, GitHub Actions, etc.), then feed the resulting PNG into your email-sending workflow of choice.
- **Image size**: `Html2Image(size=(800, 1600))` sets the render canvas; adjust the width to match your target email layout, and the height to comfortably fit your longest expected report. The auto-crop step trims the rest.

import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from docx import Document
from docx.shared import Inches, Pt, RGBColor

dummy_data = {
    'Region': ['North', 'North', 'North','South', 'South', 'South', 'East', 'East', 'East'],
    'Observation': [12, 15, 14, 8, 9, 7, 20, 18, 12]
}

df_test = pd.DataFrame(dummy_data)
print("Dummy data created successfully.")

#-----------------------------------------
#Create sample figure using the dummy data
#-----------------------------------------
sns.set_theme(style = 'whitegrid', font_scale = 0.8)
fig, ax = plt.subplots(figsize = (6, 4))

sns.boxplot(data = df_test, 
            x = 'Region', 
            y = 'Observation', 
            ax = ax, 
            color = '#16A34A')

ax.set(xlabel = 'Region',
       ylabel = 'Observation', 
       title = 'Test Plot: Regional Observations')
ax.set_ylim(bottom = 0)

#plt.show()

#save the test plot to a temporary file so it can be added to the document
#this file is not a part of the repo and will be deleted when the code is done running
#gettempdir() checks for temp folders on your machine and saves the file there; works cross-platform Windows, Mac, Linux
temp_image_path = os.path.join(tempfile.gettempdir(), 'test_plot.png')
fig.savefig(temp_image_path, bbox_inches='tight', dpi=300)

#close fig to free up memory
plt.close(fig)

#-------------------------------------------------------
#Build document from scratch and add the test plot to it
#-------------------------------------------------------

#abspath gives you the full path to the file, dirname strips away the filename and leaves you with the path to the folder
script_dir = os.path.dirname(os.path.abspath(__file__))

#initialize a new document from the template file in the repository
template_path = os.path.join(script_dir, 'Sample_Document_Template.docx')
doc = Document(template_path)

#if the template's body starts with an empty paragraph, remove it so
#our first added paragraph (the heading) isn't preceded by a blank line
if doc.paragraphs and not doc.paragraphs[0].text.strip():
    first_para = doc.paragraphs[0]
    first_para._element.getparent().remove(first_para._element)

#set document-level styles for headings and text
heading1_style = doc.styles['Heading 1']
heading1_style.font.name = 'Calibri'
heading1_style.font.size = Pt(14)
heading1_style.font.bold = True
heading1_style.font.color.rgb = RGBColor.from_string('14532D') #the from_string allows you to use hex codes

heading2_style = doc.styles['Heading 2']
heading2_style.font.name = 'Calibri'
heading2_style.font.size = Pt(12)
heading2_style.font.bold = True
heading2_style.font.color.rgb = RGBColor.from_string('000000')

normal_style = doc.styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(12)
normal_style.font.bold = False

#prepare items that will be inserted into the document
#for example, text indicating the datetime of the last data refresh
today = pd.Timestamp.today()
today_str = today.strftime("%B %d, %Y")

#create sample section heading, date of last update, and normal text below the heading
#APPROACH 1: using a predefined style (defined above) — best when you want consistent
#formatting applied automatically, every time this style is used anywhere in the document
doc.add_paragraph("Test Header", style='Heading 1')
doc.add_paragraph(f'Data last refreshed on {today_str}', style='Heading 2')
doc.add_paragraph("This is some sample text below the heading. You can add as many paragraphs as you want. This is just a placeholder for demonstration purposes.", style='Normal')

#now add the image below the text
doc.add_picture(temp_image_path, width = Inches(5))

#then add some more text below the image
doc.add_paragraph("Here is some default explanatory text below the image. You can add as many paragraphs as you want.")

#insert a page break so Approach 2 starts on its own page
#this also demonstrates that the header image repeats correctly across every page
doc.add_page_break()

#APPROACH 2 manual formatting using .add_run() — best when you want one-off formatting
#that doesn't belong to a reusable style, e.g. emphasizing a single word or a unique callout
#Note the three-step pattern: create the paragraph, add a run (text container), then format the run

#if you want plain text with just default formatting, use this code
#docx.add_paragraph("My text here")

callout_para = doc.add_paragraph()
callout_run = callout_para.add_run('Note: this paragraph is formatted manually rather than by style.')
callout_run.bold = True
callout_run.font.size = Pt(12)
callout_run.font.color.rgb = RGBColor.from_string('14532D')

#save the document to the repo
output_filename = os.path.join(script_dir, 'Sample_Document.docx')
doc.save(output_filename)

#clean up the temporary chart image now that it's embedded in the document
os.remove(temp_image_path)

print(f"Document created successfully.")
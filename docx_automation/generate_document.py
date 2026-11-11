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
            color = '#8EA49A')

ax.set(xlabel = '',
       ylabel = 'Observation (count)', 
       title = 'Distribution of Observations by Region')
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
heading1_style.font.color.rgb = RGBColor.from_string('7D9AA6') #the from_string allows you to use hex codes

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
#formatting applied automatically, every time this style is used anywhere in the document
doc.add_paragraph("Regional Observations Summary", style='Heading 1')
doc.add_paragraph(f'Data last refreshed on {today_str}', style='Heading 2')
doc.add_paragraph("This report uses synthetic data to illustrate differences in a measured environmental metric across regions.", style='Normal')

#now add the image below the text
doc.add_picture(temp_image_path, width = Inches(5))

#then add some more text below the image
doc.add_paragraph("In the figure above, the eastern region has the highest median value, and also the largest variability in observed values. The southern region had the lowest median value and the narrowest range of observed values.")

#save the document to the repo
output_filename = os.path.join(script_dir, 'Sample_Document.docx')
doc.save(output_filename)

#clean up the temporary chart image now that it's embedded in the document
os.remove(temp_image_path)

print(f"Document created successfully.")
"""
generate_deck.py
This script demonstrates how to automate the creation of a PowerPoint deck using Python.
It uses the python-pptx library to create a presentation, add slides, and insert charts and text boxes. 
The script uses matplotlib and seaborn to generate a sample chart from dummy data and adds a dynamic "Data Last Refreshed" text box.

Requirements: see requirements.txt
Usage: python generate_deck.py
Output: Sample_Deck_Updated.pptx (saved in this folder)
"""

import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

#-------------------------------------------
#define dummy data for demonstration purposes
#-------------------------------------------
test_data = {
    'Region': ['North', 'South', 'North', 'South', 'East', 'East', 'West', 'East','West'],
    'Observations': [10, 16, 9, 18, 3, 4, 2, 3, 1]
}
df_test = pd.DataFrame(test_data)

#-------------------------------------------------------------
#create a figure using the test_data to push to the slide deck
#-------------------------------------------------------------

sns.set_theme(style = 'whitegrid', font_scale = 0.8)
fig, ax = plt.subplots(figsize = (6,4))

sns.boxplot(data = df_test,
            x = 'Region',
            y = 'Observations',
            ax = ax,
            color = '#16A34A'
            )
ax.set(xlabel = 'Region',
       ylabel = 'Observations',
       title = 'Test Plot: Regional Observations')
ax.set_ylim(bottom=0)

#plt.show() #uncomment this line if you want to see the plot in a pop-up window before it is added to the slide deck

#save the test plot to a temporary file so it can be added to the slide deck
#this file is not a part of the repo and will be deleted when the code is done running
#gettempdir() checks for temp folders on your machine and saves the file there; works cross-platform Windows, Mac, Linux
temp_image_path = os.path.join(tempfile.gettempdir(), 'sample_plot.png')
fig.savefig(temp_image_path, bbox_inches = 'tight', dpi = 300)

#close fig to free up memory
plt.close(fig)

#-------------------------------------------------------------------------
#Create presentation with a template and add your image that was saved above
#Name the template file "Sample_Deck_Template.pptx" so you can reference it in the code below.
#Template must be saved to the same folder as this script for the code to work.
#-------------------------------------------------------------------------

#abspath gives you the full path to the file, dirname strips away the filename and leaves you with the path to the folder
script_dir = os.path.dirname(os.path.abspath(__file__))
existing_file_path = os.path.join(script_dir, 'Sample_Deck_Template.pptx')

#initialize the presentation using the template
if not os.path.exists(existing_file_path):
    raise FileNotFoundError(
        f"Template not found at {existing_file_path}. "
        "Make sure Sample_Deck_Template.pptx is in the same folder as this script."
    )
prs = Presentation(existing_file_path)

# #Use this code if you want to add a blank slide with a title.
# #This code uses layout #5, if you change the number it will pull a different slide layout from your demo deck template
# #We're using a template with an existing title slide so this section is commented out
# slide_layout = prs.slide_layouts[5]
# slide = prs.slides.add_slide(slide_layout)
# #Set the title text
# title = slide.shapes.title
# title.text = "Automated Deck of Regional Observations"

#Define which slides will get updated if you are adding content to an existing slide
#Remember python is zero-indexed so slide 2 is actually the third slide in the deck
chart_slide = prs.slides[2]

#Define placement of chart on slide 3
#Use inches to tell Python exactly where to place it and how big to make it
#Can position a sample figure on the page where you want it, check the position coordinates from the top left and then paste them in below
chart_left_position = Inches(3.43)
chart_top_position = Inches(1.52)
chart_image_height = Inches(4.5)

#Add chart directly to existing slide 3 in the template presentation
chart_slide.shapes.add_picture(temp_image_path, chart_left_position, chart_top_position, height = chart_image_height)

#The code below shows how you can add a text box, in this example the text box indicates the last time the code was run and the data was refreshed
refresh_slide = prs.slides[0]

#Define placement of text box on slide 1. Ge this from the position coordinates and size
text_left_position = Inches(0.83)
text_top_position = Inches(6.13)
text_width = Inches(6.4)
text_height = Inches(0.5)

#Add the text box shape to the slide first
text_box = refresh_slide.shapes.add_textbox(text_left_position, text_top_position, text_width, text_height)

#Access the box and then add the text itself
#Below I went a step further and also modified the font weight (bold) and color (blue)
today = pd.Timestamp.today()
text_frame = text_box.text_frame
text_frame.text = "" #if you want to just use the default settings put your text here and delete the next five lines
p = text_frame.paragraphs[0]
run = p.add_run()
run.text = f"Data last refreshed: {today.strftime('%m-%d-%Y')}"
run.font.name = 'Calibri'
run.font.size = Pt(24)
run.font.bold = True
run.font.color.rgb = RGBColor.from_string('DCFCE7') #this is the hex code without the # sign

output_filename = os.path.join(script_dir, 'Sample_Deck_Updated.pptx')
prs.save(output_filename)

#Clean up the temporary chart image now that it's embedded in the deck
os.remove(temp_image_path)


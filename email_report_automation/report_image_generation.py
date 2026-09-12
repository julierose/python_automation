import os
import subprocess
from html2image import Html2Image
from PIL import Image, ImageChops

def crop_whitespace(image_path, bg_color = (255, 255, 255), padding = 20):   #use 255, 255, 255 because the quarto background is #ffffff
    """Crop trailing whitespace from the bottom of an image"""
    img = Image.open(image_path).convert("RGB") 
    bg = Image.new("RGB", img.size, bg_color) #create a new plain white image the same size as your png
    diff = ImageChops.difference(img, bg) #pixel-by-pixel comparison locating content in the png
    bbox = diff.getbbox() #returns (left, upper, right, lower) of non-background content

    if bbox:
        #add a little padding below the content
        cropped = img.crop((0, 0, img.width, min(bbox[3] + padding, img.height)))
        cropped.save(image_path)
        print(f"Cropped image to content height: {cropped.height}px")
    else:
        print(" No content detected to crop against.")

def generate_html_image():
    """Convert rendered quarto html file to a png image"""
    quarto_file = "email_report_automation.qmd"
    output_html = "email_report_automation.html"
    output_image = "email_report.png"

    print(f"1. Rendering {quarto_file}")

    #render the Quarto report
    result = subprocess.run(["quarto", "render", quarto_file], capture_output=True, text=True)

    #check to see if the rendering worked
    if result.returncode == 0:
        print(" Quarto render successful.")
    else:
        print(" Error rendering Quarto file:")
        print(result.stderr)
        return

    print("2. Converting HTML to Image")

    #get working directory and create path to filename
    cwd = os.getcwd()
    html_path = os.path.join(cwd, output_html)

    hti = Html2Image(size = (800,1600)) #width is 800px

    try:
        hti.screenshot(
            html_file = html_path,
            save_as = output_image
        )
        print(f" Image saved to: {output_image}")

        print("3. Cropping excess whitespace")
        crop_whitespace(output_image)

    except Exception as e:
        print(f"An error occurred: {e}")

#only execute the function if this file is being run directly, not sourced from another script
if __name__ == "__main__":
    generate_html_image()
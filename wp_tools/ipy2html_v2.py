"""
1. Read the list of .ipynb files from list.csv in same folder
2. For each file, create respective html 
3. Fix 100% width issue for SVG element (CSS) for each html
4. write html in current folder
"""

import nbformat
import nbconvert
import sys
import os
import ntpath

# 1. Read the list of .ipynb files from list.csv in same folder
import csv
with open('list.csv') as csvfile:
    ipynb_reader = csv.reader(csvfile)
    for each_row in ipynb_reader:
        current_file =  each_row[0]
        print(current_file)

        """
        2. For each file, create respective html 
        https://github.com/jupyter/nbconvert/issues/699
        """
        with open(current_file, 'rb') as nb_file:
            nb_contents = nb_file.read().decode('utf8')  

        # Convert using the ordinary exporter
        notebook = nbformat.reads(nb_contents, as_version=4)      
        outname = ntpath.basename(current_file)
        outname = outname.split('.ipynb')[0] + '.html'
        print("Converting to HTML:", outname)
        exporter = nbconvert.HTMLExporter()
        body, res = exporter.from_notebook_node(notebook)        

        # Create a list saving all image attachments to their base64 representations
        images = []
        for cell in notebook['cells']:
            if 'attachments' in cell:
                attachments = cell['attachments']
                for filename, attachment in attachments.items():
                    for mime, base64 in attachment.items():
                        images.append( [f'attachment:{filename}', f'data:{mime};base64,{base64}'] )

        # Fix up the HTML and write it to disk
        for itmes in images:
            src = itmes[0]
            base64 = itmes[1]
            body = body.replace(f'src="{src}"', f'src="{base64}"', 1)  


        with open(outname, 'w') as output_file:
            output_file.write(body)   

        #print('{} is done'.format(each_row[0]))   
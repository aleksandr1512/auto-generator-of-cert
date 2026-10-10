import fitz
import pandas as pd
import shutil
import os
import streamlit as st


def replace_text_in_pdf(input_pdf, output_pdf, replacements, font_size=14):
    doc = fitz.open(input_pdf)
    
    for page in doc:
        text_instances = page.search_for("{{Фамилия, имя участника 1}}")
        font_name = page.insert_font(fontname="my_russian_font", fontfile="fonts/Gilroy-Light.otf")
        
        for rect in text_instances:
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            
            point = fitz.Point(rect.x0, rect.y1 - 2) 
            page.insert_text(
                point, 
                replacements[0], 
                fontsize=font_size, 
                fontname="my_russian_font",
                color=(0, 0, 0)
            )

        text_instances1 = page.search_for("{{Название образовательного учреждения (кратко)}}")
        
        for rect in text_instances1:
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            
            point = fitz.Point(rect.x0, rect.y1 - 2) 
            page.insert_text(
                point, 
                replacements[1], 
                fontsize=font_size, 
                fontname="my_russian_font",
                color=(0, 0, 0)
            )
            
    doc.save(output_pdf)
    doc.close()

def excel_to_pdfs(excel_file, archive_path):
    try:
        df = pd.read_excel(excel_file)

        for index,row in df.iterrows():
            if row['Фамилия, имя участника 1'] != "":
                replace_text_in_pdf("templates/SertificateTemplate.pdf", f"certs/{row['Фамилия, имя участника 1']}.pdf", [row['Фамилия, имя участника 1'],row['Название образовательного учреждения (кратко)']])

        shutil.make_archive(archive_path, 'zip', 'certs')

        folder_path = 'certs'

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Удаляет папку вместе со всем содержимым

        os.makedirs(folder_path)

        return 0
    except:
        return 1
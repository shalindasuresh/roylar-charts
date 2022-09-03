import streamlit as st
import json
from sjvisualizer import DataHandler, Canvas, BarRace, StaticImage
st.set_page_config(layout="centered", page_icon="", page_title="Diploma Generator")
st.title("Synapsis Graph Generator")
from PIL import Image
#image = Image.open('logo.jpg')
#st.image(image, caption='')
st.subheader("In this website you can submit your CSV or Excel sheet and it will be "
        "converted into a moving graph video!")

uploaded_file = st.file_uploader("Choose a file")
print(uploaded_file)
left, right = st.columns(2)
form = left.form("template_form")
title = form.text_input("Title")
subtitle = form.text_input("Subtitle")
durat = form.slider("Duration in seconds", 1, 3, 2)
submit = form.form_submit_button("Generate Visualization")

EXCEL_FILE = "data/"+str(uploaded_file.name)
print(EXCEL_FILE)
FPS = 60
DURATION = int(durat)


if submit:
     try:
          df = DataHandler.DataHandler(excel_file=EXCEL_FILE, number_of_frames=FPS * DURATION * 60).df
          canvas = Canvas.canvas()

          bar_chart = BarRace.bar_race(df=df, canvas=canvas.canvas)
          canvas.add_sub_plot(bar_chart)

     # adding a title
          canvas.add_title(title, color=(0, 0, 0))
          canvas.add_sub_title(subtitle, color=(150, 150, 150))

     # adding a time
          canvas.add_time(df=df, time_indicator="year")

     # play the animation
          canvas.play(fps=FPS)
     except Exception as e:
          st.write('Windows Closed')
          # st.write("ERRORS")
          st.write(str(e))
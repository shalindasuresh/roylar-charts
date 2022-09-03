import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
from raceplotly.plots import barplot
from collections import deque



    #Add a file uploader to allow users to upload their csv file
st.markdown(""" <style> .font {
font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Upload your data...</p>', unsafe_allow_html=True) #use st.markdown() with CSS style to create a nice-formatted header/text

uploaded_file = st.file_uploader('',type=['xls','xlsx']) #Only accepts csv file format
if uploaded_file is not None:     
     df=pd.read_excel(uploaded_file)  #use AgGrid to create a aggrid table that's more visually appealing than plain pandas datafame
     # grid_response = AgGrid(            
     #      df,
     #      editable=False, 
     #      height=300, 
     #      fit_columns_on_grid_load=True,
     #      theme='alpine',
     #      width=100,
     #      allow_unsafe_jscode=True,
     #      )
     # updated = grid_response['data']  
     df = pd.DataFrame(df) 
     
     # raceplot = barplot(df,  item_column='Argentina', value_column='Argentina', time_column='Argentina')

     # raceplot.plot(item_label = 'Top 10 Countries', value_label = 'GDP ($)', frame_duration = 800)

     st.write('---')
     st.markdown('<p class="font">Set Parameters...</p>', unsafe_allow_html=True)
     column_list=list(df)
     column_list = deque(column_list)
     column_list.appendleft('-')
     with st.form(key='columns_in_form'):
          text_style = '<p style="font-family:sans-serif; color:red; font-size: 15px;">***These input fields are required***</p>'
          st.markdown(text_style, unsafe_allow_html=True)
          col1, col2, col3 = st.columns( [1, 1, 1])
          with col1:
               item_column=st.selectbox('Bar column:',column_list, index=0, help='Choose the column in your data that represents the bars, e.g., countries, teams, etc.') 
          with col2:    
               value_column=st.selectbox('Metric column:',column_list, index=0, help='Choose the column in your data that represents the value/metric of each bar, e.g., population, gdp, etc.') 
          with col3:    
               time_column=st.selectbox('Time column:',column_list, index=0, help='Choose the column in your data that represents the time series, e.g., year, month, etc.')   

          text_style = '<p style="font-family:sans-serif; color:blue; font-size: 15px;">***Customize and fine-tune your plot (optional)***</p>'
          st.markdown(text_style, unsafe_allow_html=True)
          col4, col5, col6 = st.columns( [1, 1, 1])
          with col4:
               direction=st.selectbox('Choose plot orientation:',['-','Horizontal','Vertical'], index=0, help='Specify whether you want the bar chart race to be plotted horizontally or vertically. The default is horizontal' ) 
               if direction=='Horizontal'or direction=='-':
                orientation='horizontal'
               elif  direction=='Vertical':   
                orientation='vertical'
          with col5:
               item_label=st.text_input('Add a label for bar column:', help='For example: Top 10 countries in the world by 2020 GDP')  
          with col6:
               value_label=st.text_input('add a label for metric column', help='For example: GDP from 1965 - 2020') 

          col7, col8, col9 = st.columns( [1, 1, 1])
          with col7:
               num_items=st.number_input('Choose how many bars to show:', min_value=5, max_value=50, value=10, step=1,help='Enter a number to choose how many bars ranked by the metric column. The default is top 10 items.')
          with col8:
               format=st.selectbox('Show by Year or Month:',['-','By Year','By Month'], index=0, help='Choose to show the time series by year or month')
               if format=='By Year' or format=='-':
                    date_format='%Y'
               elif format=='By Month':
                    date_format='%x'   
          with col9:
               chart_title=st.text_input('Add a chart title', help='Add a chart title to your plot')    
          
          col10, col11, col12 = st.columns( [1, 1, 1])
          with col10:
               speed=st.slider('Animation Speed',10,500,100, step=10, help='Adjust the speed of animation')
               frame_duration=500-speed  
          with col11:
               chart_width=st.slider('Chart Width',500,1000,500, step=20, help='Adjust the width of the chart')
          with col12:    
               chart_height=st.slider('Chart Height',500,1000,600, step=20, help='Adjust the height of the chart')

          submitted = st.form_submit_button('Submit')
          


     st.write('---')
     if submitted:        
               if item_column=='-'or value_column=='-'or time_column=='-':
                    st.warning("You must complete the required fields")
               else: 
                    st.markdown('<p class="font">Generating your bar chart race plot... And Done!</p>', unsafe_allow_html=True)   
                    df['time_column'] = pd.to_datetime(df[time_column])
                    df['value_column'] = df[value_column].astype(float)

                    raceplot = barplot(df,  item_column=item_column, value_column=value_column, time_column=time_column,top_entries=num_items)
                    fig=raceplot.plot(item_label = item_label, value_label = value_label, frame_duration = frame_duration, date_format=date_format,orientation=orientation)
                    fig.update_layout(
                    title=chart_title,
                    autosize=False,
                    width=chart_width,
                    height=chart_height,
                    paper_bgcolor="lightgray",
                    )
                    st.plotly_chart(fig, use_container_width=True)
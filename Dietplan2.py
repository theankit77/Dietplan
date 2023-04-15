import streamlit as st
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import openai
from tabulate import tabulate
from PIL import Image
import pandas as pd
from termcolor import colored

openai.api_key = "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"

st.set_page_config(
    page_title="DietChart",
    initial_sidebar_state="collapsed", 
    page_icon="ðŸ“ˆ"
)

st.markdown("<style> .e1fqkh3o1 {display: none;} </style>", unsafe_allow_html=True)

st.markdown("# Your Healthy 6 week Weight Loss Goal")


with st.form(key='2_form'):
	Name = st.text_input("Enter your name:")
	Email = st.text_input("Enter your Email:")
	Age = st.text_input("Enter your Age(years):")
	Height = st.text_input("Enter your Height(cm):")
	Curr_Weight = st.text_input("Enter your current weight(kg):")
	Tar_Weight = st.text_input("What's your 6 week weight loss goal(kg):")
	Type_of_Diet = st.text_input("What kind of diet you prefers? ")
	submit_button = st.form_submit_button(label='Generate Diet Plan')
	if submit_button:		
		query = "{} whose age is {} years whose height is {}cm and weight is {}kg has a goal of reducing his weight to {}kg in 6 weeks . Create a 1 week whole {} weekly eating plan (Mon-Sat) with 3 meals per day which Steve has to follow for 6 weeks regularly to  achieve his desired weight.Write a 1 line introduction.".format(Name,Age,Height,Curr_Weight,Tar_Weight,Type_of_Diet)
		response = openai.Completion.create(
					engine= "text-davinci-003",
					prompt=query,
					temperature=0.7,
					max_tokens=2056,
					top_p=1,
					frequency_penalty=0,
					presence_penalty=0)
		ac1 = response['choices'][0]['text'];
		query = "{} whose age is {} years whose height is {}cm and weight is {}kg has a goal of reducing his weight to {}kg in 6 weeks . Create a 1 week whole {} weekly eating plan (Mon-Sat) with 3 meals per day which Steve has to follow for 6 weeks regularly to  achieve his desired weight.For Breakfast, Lunch and Dinner please specify diet in grams and calories clearly.Format it as JSON string without any headings.".format(Name,Age,Height,Curr_Weight,Tar_Weight,Type_of_Diet)
		response = openai.Completion.create(
					engine= "text-davinci-003",
					prompt=query,
					temperature=0.7,
					max_tokens=2056,
					top_p=1,
					frequency_penalty=0,
					presence_penalty=0)
		ac2 = response['choices'][0]['text'];
		print(ac2)
		df = pd.read_json(ac2)
		for i in range(6):
			for j in range(3):
				s = ''
				for a,b in zip(df.iloc[j,i].keys(),df.iloc[j,i].values()): 
					s = s+str(a)+':'+str(b)+' ' 
				df.iloc[j,i] = s
		final = pd.DataFrame.transpose(df)
		print(final)
		query = "This is the diet plan {} to be followed for 6 weeks.Write a conclusion for this diet plan.".format(ac2)
		response = openai.Completion.create(
					engine= "text-davinci-003",
					prompt=query,
					temperature=0.7,
					max_tokens=2048,
					top_p=1,
					frequency_penalty=0,
					presence_penalty=0)
		ac3 = response['choices'][0]['text'];
		from tabulate import tabulate
		Table = tabulate(final, headers = 'keys', tablefmt = 'psql')
		print(Table)
		final.reset_index(level = 0, inplace = True)
		final.rename(columns = {'index':'Weekday'},inplace=True)
		final
		narrow_table = pd.melt(final, id_vars='Weekday', value_vars=['Breakfast', 'Lunch', 'Dinner'])
		# Custom title, introduction, and conclusion
		title = colored('                                                                              6 WEEK WEIGHT LOSS CHALLENGE', attrs=['bold'])
		introduction = ac1
		conclusion = ac3

		# Convert the DataFrame to a formatted table string
		df_table = narrow_table.to_string(index=False)

		# Create a text file and write the title, introduction, DataFrame as a table, and conclusion
		with open('Dietplan.txt', 'w') as f:
			f.write(title + '\n\n')
			f.write(introduction + '\n\n')
			f.write('Diet Plan:\n\n')
			f.write(df_table + '\n\n\n')
			f.write('Conclusion:')
			f.write(conclusion + '\n')

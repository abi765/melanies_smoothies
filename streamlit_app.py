# Import python packages
import streamlit as st
import requests
import pandas as pd

# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Attempt to connect to Snowflake
try:    # Remove this line
    cnx = st.connection("snowflake")
    session = cnx.session()
    st.success("Connected to snowfalke!") # Remove this line
except Exception as e: # Remove this line
    st.error(f"Error connecting to Snowflake: {str(e)}") # Remove this line
    st.stop() # Remove this line

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

# import streamlit as st
name_on_order = st.text_input('Name of Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the Snowpark Dataframe in a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to.pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )
if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
        fv_df = st. dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        # st.success('Your Smoothie is ordered!', icon="✅" +'May')
        # st.success('Your Smoothie is ordered! ' + "✅ " + name_on_order)
        st.success("✅ " + "Your Smoothie is ordered, " + name_on_order + "!")




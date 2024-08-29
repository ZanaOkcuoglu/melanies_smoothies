import streamlit as st
from snowflake.snowpark.context import get_active_session

# Set up the Streamlit app title and introduction
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write(
    """
    **Choose the fruits you want in your custom Smoothie!**
    """
)

# Get the active Snowflake session
session = get_active_session()

# Fetch only the relevant column from the Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

# Collect the fruit names as a list
fruit_list = my_dataframe.collect()

# Extract the actual fruit names from the Snowflake Row objects
fruit_names = [row['FRUIT_NAME'] for row in fruit_list]

# Create a multi-select widget for the user to choose ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    fruit_names,  # Pass the list of fruit names to the multi-select widget
    max_selections=5
)

# Display the selected ingredients using Streamlit
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

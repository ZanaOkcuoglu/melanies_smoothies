import streamlit as st
from snowflake.snowpark.functions import col

# Set up the Streamlit app title and introduction
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write(
    """
    **Choose the fruits you want in your custom Smoothie!**
    """
)

name_on_order = st.text_input('Name on the Smoothie')
st.write("Name on the Smoothie is", name_on_order)

# Get the Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch only the relevant column from the Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")
fruit_list = my_dataframe.collect()
fruit_names = [row['FRUIT_NAME'] for row in fruit_list]

# Create a multi-select widget for the user to choose ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    fruit_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            # Use parameterized query to prevent SQL injection
            insert_stmt = """
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES (?, ?)
            """
            session.sql(insert_stmt).bind_params(ingredients_string, name_on_order).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Set up the Streamlit app title and introduction
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write("**Choose the fruits you want in your custom Smoothie!**")

# Input for user's name on the smoothie order
name_on_order = st.text_input('Name on the Smoothie')
st.write("Name on the Smoothie is", name_on_order)

# Establish connection to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch the fruit names and their search terms from the Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME", "SEARCH_ON")
fruit_list = my_dataframe.collect()

# Create a dictionary mapping fruit names to their search terms
fruit_search_dict = {row['FRUIT_NAME']: row['SEARCH_ON'] for row in fruit_list}

# Extract the actual fruit names for the multi-select widget
fruit_names = list(fruit_search_dict.keys())

# Create a multi-select widget for the user to choose ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    fruit_names,
    max_selections=5
)

# Display the selected ingredients and prepare SQL insert statement
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    for fruit_chosen in ingredients_list:
        st.subheader(f'{fruit_chosen} Nutrition Information')
        search_term = fruit_search_dict[fruit_chosen]
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_term}")
        if fruityvice_response.status_code == 200:
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        else:
            st.error(f"Couldn't find nutrition information for {fruit_chosen}")

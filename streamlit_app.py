import streamlit as st
from snowflake.snowpark.functions import col

# Set up the Streamlit app title and introduction
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write(
    """
    **Choose the fruits you want in your custom Smoothie!**
    """
)

# Input for user's name on the smoothie order
name_on_order = st.text_input('Name on the Smoothie')
st.write("Name on the Smoothie is", name_on_order)

# Establish connection to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

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

# Display the selected ingredients and prepare SQL insert statement
if ingredients_list:
    # Combine selected ingredients into a single string
    ingredients_string = ', '.join(ingredients_list)

    # Prepare the SQL insert statement using placeholders to avoid SQL injection
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (%s, %s)
    """

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            # Execute the SQL statement with parameters
            session.execute(my_insert_stmt, (ingredients_string, name_on_order))
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            # Display the error if any occurs
            st.error(f"An error occurred: {str(e)}")

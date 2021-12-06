# Walker Frankenberg & Daniel Brey
# 30 October 2021
# Adapted from https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030

import streamlit as st

# Define the multipage class to manage the multiple pages in our program 
class MultiPage: 

    # Constructor to create a list to store all the pages
    def __init__(self):
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    # Method to add a page to the list of pages
    # Args:
    #   title ([str]): The title of page which we are adding to the list of apps
    #   func: Python function to render this page in Streamli
    def add_page(self, title, func): 
        self.pages.append({"title": title, 
                          "function": func})

    # Run the app function
    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'Page Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        page['function']()
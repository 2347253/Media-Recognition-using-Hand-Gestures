import streamlit as st
from home import main as home_page
from main_functionality import main as functionality_page
from about import main as about_page

def main():
    # Display profile picture in circular view
    st.sidebar.image("shawn.png", use_column_width=True, output_format='JPEG', width=5, caption="ST Media")
    
    # Centered title
    st.markdown("<h1 style='text-align: center;'>🎬 Media control with Hand Gestures</h1>", unsafe_allow_html=True)
    
    # Navigation bar
    st.sidebar.title("Navigation")
    pages = ["Home", "Main Functionality", "About"]
    selected_page = st.sidebar.selectbox("Select Page", pages)

    if selected_page == "Home":
        home_page()
    elif selected_page == "Main Functionality":
        functionality_page()
    elif selected_page == "About":
        about_page()

if __name__ == "__main__":
    main()

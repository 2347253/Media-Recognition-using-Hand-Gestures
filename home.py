import streamlit as st

def main():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Hello there! Welcome to my project on controlling media with hand gestures.</h3>", unsafe_allow_html=True)
    st.markdown("<h4>Here's how to use this application:</h4>", unsafe_allow_html=True)
    
    st.markdown("🖐️ -  Show your Left palm to Play the video.")
    st.markdown("✊ -  Show your Left fist to Stop the video.")
    st.markdown("👌 -  Pinch in with your Right Hand to Reduce the volume.")
    st.markdown("🤏 -  Pinch out with your Right Hand to Increase the volume.")

if __name__ == "__main__":
    main()

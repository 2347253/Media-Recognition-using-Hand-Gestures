import streamlit as st

def main():
    st.markdown("<h3>About Us</h3>", unsafe_allow_html=True)
    st.write("Media Control with Hand Gestures is an innovative project that allows users to interact with media content using simple hand gestures. Gone are the days of relying solely on remote controls or keyboard shortcuts to manage your video playback experience. With this project, you can harness the power of hand gestures to effortlessly control media playback on your device.")

    st.write("It provides a seamless and intuitive way to navigate through your favorite videos without ever needing to touch a physical input device.")
    st.markdown("<h3>Key Gestures and Actions:</h3>", unsafe_allow_html=True)

    st.write("🖐️ Play/Pause: Show your left palm to play the video. When you want to pause, simply show your left fist.")
    st.write("👌 Volume Control: Use your right hand to control the volume. Pinch in to decrease the volume, and pinch out to increase it.")

    st.markdown("<h3>Output Screens :</h3>", unsafe_allow_html=True)
    
    st.image("scr1.png", caption="Screenshot 1 - Decrease", use_column_width=True)
    st.image("scr2.png", caption="Screenshot 2 - Increase", use_column_width=True)
    st.image("scr3.png", caption="Screenshot 3 - Play", use_column_width=True)
    st.image("scr4.png", caption="Screenshot 3 - Stop", use_column_width=True)

if __name__ == "__main__":
    main()

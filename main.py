import streamlit as st
import os

# Folder to save files
SAVE_DIR = "files"
os.makedirs(SAVE_DIR, exist_ok=True)

st.title("SeaSentinel 👋")

# File uploader (image or video)
uploaded_file = st.file_uploader(
    "Upload an image or video",
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"]
)

# Description input
description = st.text_area("Enter description")

# Location input
location = st.text_input("Enter location name")


# Show preview of file
if uploaded_file is not None:
    file_type = uploaded_file.type
    if "image" in file_type:
        st.image(uploaded_file, caption="Preview", width="content")
    elif "video" in file_type:
        st.video(uploaded_file)


# Save everything locally
if st.button("Save Locally"):
    if uploaded_file and description and location:
        # Save file
        file_path = os.path.join(SAVE_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Save metadata (description + location) in a text file
        meta_path = os.path.join(SAVE_DIR, uploaded_file.name + ".txt")
        with open(meta_path, "w") as f:
            f.write(f"Description: {description}\n")
            f.write(f"Location: {location}\n")

        st.success(f"✅ File and details saved in {SAVE_DIR}/")
    else:
        st.warning("Please upload a file, add description, and enter location before saving.")

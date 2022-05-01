"""Create an Image Classification Web App using PyTorch and Streamlit."""
# import libraries
from PIL import Image
from io import BytesIO
import streamlit as st
from requests_futures.sessions import FuturesSession

session = FuturesSession()

# set title of app
st.title("Simple Image Classification Application")
st.write("")

# enable users to upload images for the model to make predictions
file_up = st.file_uploader("Upload an image", type = ['png', 'jpg', "jpeg", "PNG", "JPG"])

if file_up is not None:
    # display image that user uploaded
    image = Image.open(file_up)
    mem_file_c = BytesIO()
    image.save(mem_file_c, "PNG", quality=100)
    mem_file_c.seek(0)
    st.image(image, caption = 'Uploaded Image.', use_column_width = True)
    st.write("")
    st.write("Just a second ...")
    r = session.post(
        f"http://backend:8000/predict",
        files={
            'image_c': ('file_c.PNG', mem_file_c, 'image/png')
        }
    )
    labels = r.result().json()["labels"]
    # print out the top 5 prediction labels with scores
    for i in labels:
        st.write("Prediction (index, name)", i[0], ",   Score: ", i[1])

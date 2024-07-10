import streamlit as st
import mysql.connector
from mysql.connector import Error
from PIL import Image, UnidentifiedImageError
import io
import requests

def insert_image(connection, cursor, image_name, image_data):
    try:
        cursor.execute("INSERT INTO images (image_name, image_data) VALUES (%s, %s)", (image_name, image_data))
        connection.commit()
        st.success("Image inserted successfully.")
    except Error as e:
        connection.rollback()
        st.error(f"Error inserting image: {e}")

def retrieve_images(connection, cursor):
    try:
        cursor.execute("SELECT image_name, image_data FROM images")
        rows = cursor.fetchall()
        images = []
        for row in rows:
            image_name, image_data = row
            try:
                image = Image.open(io.BytesIO(image_data))
                images.append((image_name, image, image_data))
            except UnidentifiedImageError:
             #   st.error(f"Unidentified image error for image: {image_name}")
                continue
        return images
    except Error as e:
        st.error(f"Error retrieving images: {e}")
        return []

def fetch_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = response.content
        image_name = url.split("/")[-1]
        return image_name, image_data
    except requests.RequestException as e:
        st.error(f"Error fetching image from URL: {e}")
        return None, None

def main():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='webdata',
            user='root',
            password='Purv@19205'
        )

        cursor = connection.cursor()

        st.title("Upload and Retrieve Images from Database")

        uploaded_file = st.file_uploader("Choose an image from your system...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image_data = uploaded_file.read()
            image_name = uploaded_file.name
            insert_image(connection, cursor, image_name, image_data)

        image_url = st.text_input("Or enter the URL of an image...")
        if st.button("Upload Image from URL"):
            if image_url:
                image_name, image_data = fetch_image_from_url(image_url)
                if image_name and image_data:
                    insert_image(connection, cursor, image_name, image_data)

        if st.button("Get All Images"):
            images = retrieve_images(connection, cursor)
            if images:
                cols = st.columns(3)
                for idx, (image_name, image, image_data) in enumerate(images):
                    col = cols[idx % 3]
                    with col:
                        st.image(image, caption=image_name)
                        st.download_button(
                            label="Download Image",
                            data=image_data,
                            file_name=image_name,
                            mime="image/jpeg" if image_name.endswith("jpg") or image_name.endswith("jpeg") else "image/png",
                            key=f"download_button_{idx}_{image_name}"
                        )
            else:
                st.info("No images found in the database.")

    except Error as e:
        st.error(f"Database connection error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()

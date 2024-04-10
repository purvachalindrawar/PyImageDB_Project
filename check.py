import mysql.connector
from mysql.connector import Error

def insert_image(connection, cursor, image_name, image_data):
    try:
        cursor.execute("INSERT INTO images (image_name, image_data) VALUES (%s, %s)", (image_name, image_data))
        connection.commit()
        print("Image inserted successfully.")

    except Error as e:
        connection.rollback()
        print(f"Error inserting image: {e}")

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='webdata',
        user='root',
        password='Purv@19205'
    )

    cursor = connection.cursor()

    
    file_path = input("Enter the file path of the image: ")

    
    with open(file_path, 'rb') as file:
        image_data = file.read()

   
    image_name = file_path.split('/')[-1]  # Assuming Unix-style path separator

    insert_image(connection, cursor, image_name, image_data)

except FileNotFoundError:
    print("Error: File not found.")

except Error as e:
    print(f"Database connection error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

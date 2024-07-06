import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost', 
        database='webdata',  
        user='root',  
        password='Purv@19205'  
    )

    cursor = connection.cursor()
    cursor.execute("SELECT image_data FROM webdata.storing WHERE image_name = 'C:\Users\chali\Downloads\sign.jpg'")
    result = cursor.fetchone()

    if result:
        image_data = result[0]

        with open('image.png', 'wb') as file:  
            file.write(image_data)

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

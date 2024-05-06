from flask import Blueprint, Flask, render_template, request, send_file
import mysql.connector
import qrcode
import hashlib
import io

# Database credentials and other code
db_host = 'host.docker.internal'
db_port = 3306
db_user = 'm169databaseadmin'
db_password = 'abcd12s8rkds'
db_name = 'm169database'

# Connect to the database
db = mysql.connector.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_name
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Create the necessary tables if they don't exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

# Create manufacturers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS manufacturers (
        id_manufacturer INT AUTO_INCREMENT PRIMARY KEY,
        name_manufacturer VARCHAR(255),
        email_manufacturer VARCHAR(255),
        number_manufacturer VARCHAR(255),
        website_manufacturer VARCHAR(255),
        manufacturer_hash VARCHAR(128)
    )
""")

# Create QRCode table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qrcode (
        id_qrcode INT AUTO_INCREMENT PRIMARY KEY,
        id_manufacturer INT,
        qrcode_hash VARCHAR(128),
        FOREIGN KEY (id_manufacturer) REFERENCES manufacturers(id_manufacturer)
    )
""")

inserter_bp = Blueprint('inserter', __name__, template_folder='../templates')

@inserter_bp.route('/inserter', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        website = request.form['website']

        # Check if the manufacturer already exists in the database
        select_query = "SELECT * FROM manufacturers WHERE name_manufacturer = %s"
        cursor.execute(select_query, (name,))
        manufacturer = cursor.fetchone()

        # Generate SHA-512 hash for the manufacturer
        manufacturer_hash = hashlib.sha512(name.encode()).hexdigest()

        if manufacturer:
            # Manufacturer already exists, update the existing record
            update_query = "UPDATE manufacturers SET email_manufacturer = %s, number_manufacturer = %s, website_manufacturer = %s, manufacturer_hash = %s WHERE id_manufacturer = %s"
            cursor.execute(update_query, (email, number, website, manufacturer_hash, manufacturer[0]))
            db.commit()
        else:
            # Manufacturer doesn't exist, insert a new record
            insert_query = "INSERT INTO manufacturers (name_manufacturer, email_manufacturer, number_manufacturer, website_manufacturer, manufacturer_hash) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (name, email, number, website, manufacturer_hash))
            db.commit()

            # Get the last inserted manufacturer ID
            manufacturer_id = cursor.lastrowid

            # Generate SHA-512 hash for the QR code
            qrcode_hash = hashlib.sha512(str(manufacturer_id).encode()).hexdigest()

            # Insert QR Code into the database
            insert_qrcode_query = "INSERT INTO qrcode (id_manufacturer, qrcode_hash) VALUES (%s, %s)"
            cursor.execute(insert_qrcode_query, (manufacturer_id, qrcode_hash))
            db.commit()

    return render_template('inserter.html')


@inserter_bp.route('/get_qrcode/<int:qrcode_id>', methods=['GET'])
def get_qrcode(qrcode_id):
    # Retrieve manufacturer ID and QR Code hash from the database based on qrcode_id
    select_qrcode_query = "SELECT id_manufacturer, qrcode_hash FROM qrcode WHERE id_qrcode = %s"
    cursor.execute(select_qrcode_query, (qrcode_id,))
    qr_code_data = cursor.fetchone()

    if qr_code_data:
        manufacturer_id = qr_code_data[0]
        qrcode_hash = qr_code_data[1]

        # Retrieve manufacturer details based on manufacturer_id
        select_manufacturer_query = "SELECT name_manufacturer, website_manufacturer FROM manufacturers WHERE id_manufacturer = %s"
        cursor.execute(select_manufacturer_query, (manufacturer_id,))
        manufacturer_data = cursor.fetchone()

        if manufacturer_data:
            name = manufacturer_data[0]
            website = manufacturer_data[1]

            # Generate QR Code data
            qr_code_data = f"Manufacturer ID: {manufacturer_id}\nName: {name}\nQR Code Hash: {qrcode_hash}\nManufacturer Website: {website}\nQuery: /fetch?id={qrcode_id}"

            # Generate QR Code image
            qr_code = qrcode.QRCode(
                version=10,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr_code.add_data(qr_code_data)
            qr_code.make(fit=True)

            qr_code_image = qr_code.make_image(fill_color="black", back_color="white")

            # Save QR Code image to a BytesIO object
            qr_code_image_io = io.BytesIO()
            qr_code_image.save(qr_code_image_io, format='PNG')
            qr_code_image_io.seek(0)  # Reset the file position to the beginning before reading its contents

            # Send the QR Code image as a file to the client
            return send_file(qr_code_image_io, mimetype='image/png')
        else:
            return 'Manufacturer not found.'
    else:
        return 'QR Code not found.'


app = Flask(__name__)
app.register_blueprint(inserter_bp)

if __name__ == '__main__':
    app.run()
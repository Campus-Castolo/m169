from flask import Blueprint, request, render_template
import mysql.connector
import qrcode
from io import BytesIO
import base64

fetcher_bp = Blueprint('fetcher', __name__, template_folder='../templates')

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

@fetcher_bp.route('/fetch', methods=['GET', 'POST'])
def fetch():
    qr_codes_data = None

    if request.method == 'POST':
        # Retrieve form data
        manufacturer_id = request.form.get('manufacturer_id')
        manufacturer_name = request.form.get('manufacturer_name')

        if manufacturer_id:
            # Fetch the QR codes for the given manufacturer_id
            query = """
                SELECT q.id_qrcode, q.qrcode_hash, m.name_manufacturer
                FROM qrcode q
                INNER JOIN manufacturers m ON q.id_manufacturer = m.id_manufacturer
                WHERE m.id_manufacturer = %s
            """
            cursor.execute(query, (manufacturer_id,))
            qr_codes_data = cursor.fetchall()

        elif manufacturer_name:
            # Fetch the QR codes for the given manufacturer_name
            query = """
                SELECT q.id_qrcode, q.qrcode_hash, m.name_manufacturer
                FROM qrcode q
                INNER JOIN manufacturers m ON q.id_manufacturer = m.id_manufacturer
                WHERE m.name_manufacturer = %s
            """
            cursor.execute(query, (manufacturer_name,))
            qr_codes_data = cursor.fetchall()

        # Generate QR code images for each QR code data
        qr_codes_with_images = []
        for qr_code in qr_codes_data:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_code[1])  # QR code data
            qr.make(fit=True)

            # Generate the QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Encode the image in base64
            buffered = BytesIO()
            qr_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Construct the data URI for embedding in HTML
            qr_code_with_image = {
                'id': qr_code[0],
                'manufacturer': qr_code[2],
                'qrcode_hash': qr_code[1],
                'qr_img_url': f"data:image/png;base64,{img_str}"
            }
            qr_codes_with_images.append(qr_code_with_image)

        qr_codes_data = qr_codes_with_images

    return render_template('fetch.html', qr_codes=qr_codes_data)

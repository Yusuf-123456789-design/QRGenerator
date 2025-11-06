from flask import Flask, request, send_file, jsonify
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "QR Code Generator API is running!"})

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    """
    Dynamically generates a QR code from ANY user details sent as JSON.
    Example:
    {
        "name": "shaik yusuf",
        "email": "yusuf.g@nichebit.com",
        "phone": "9876543210",
        "father name": "saida",
        "mother name": "ramzanbi",
        "brother name": "salim"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body found"}), 400

    # Build QR content dynamically from all fields
    qr_text = "\n".join([f"{key.title()}: {value}" for key, value in data.items()])

    # Generate smaller QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to buffer
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    # Return QR image directly
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)

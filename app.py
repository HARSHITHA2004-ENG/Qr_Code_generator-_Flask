from flask import Flask ,render_template, request , jsonify
import qrcode
import io
import base64
app = Flask(__name__)

@app.route('/')
def index():
    """
    This functiom handles GET request to thr rool URL(/)
    It renders and returns the HTML Template (inde.html)"""
    return render_template('index.html')
@app.route('/generate_qr',methods=['POST'])
def generate_qr():
    """
This function handelspost request from html js  .It recives text data , denerate QR code , adn retun IMage as base64"""
    try:
        data =  request.json
        text = data.get('text','')

        if not text:
            return jsonify({'error':'No text Provided'}) ,400
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size = 10,
            border =4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black",back_color="white")

        buffered =io.BytesIO()
        img.save(buffered ,format ="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            'success' :True,
            'image':f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        print(f"Error generating QR code:{str(e)}")
        return jsonify({'error':str(e)}),500
    
if __name__ == '__main__':
    app.run(debug=True)
    






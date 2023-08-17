import barcode
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from pathlib import Path
# Import the card creation code here (the create_card function)
# ...
# ...

from PIL import Image, ImageDraw, ImageFont

def create_card(data):
    # Create a blank card with a white background
    def generate_barcode(data):
        # Create the barcode object
        barcode_class = Code128(data["membership_no"], writer=ImageWriter())

        # Save the barcode as an image
        barcode_image = BytesIO()
        barcode_class.write(barcode_image)
        return barcode_image
    barcode_image=generate_barcode(data)
    card_width, card_height = 1000, 1000
    card = Image.new('RGB', (card_width, card_height), color='#001f3f')
    draw = ImageDraw.Draw(card)

    # Add the barcode image to the card
    barcode_image = Image.open(barcode_image)
    dufa_image = Image.open(Path(__file__).parent.parent /"static"/ 'dufa.png')
    udsm_image = Image.open(Path(__file__).parent.parent /"static" /'udsm_screen.png')
    card.paste(dufa_image, (0, 0))
    card.paste(udsm_image, (750, 0))
    card.paste(barcode_image, (350, 750))

    # Add other information to the card
    font = ImageFont.truetype(str(Path(__file__).parent.parent /"static"/ 'Arial.ttf'), 40)
    draw.text((10, 300), f"Memb No: {data['membership_no']}", fill='white', font=font)
    draw.text((10, 360), f"Name: {(data['first_name'] + '  ' + data['surname'])}", fill='white', font=font)
    draw.text((10, 420), f"Phone: {data['phone_number']}", fill='white', font=font)
    draw.text((10, 480), f"Email: {data['email']}", fill='white', font=font)

      # Save the card as bytes
    card_bytes_io = BytesIO()
    card.save(card_bytes_io, format='PNG')

    # Seek to the beginning of the BytesIO object
    card_bytes_io.seek(0)

    return card_bytes_io.getvalue()


def send_email_with_attachment(data,email):
    # Generate the card image as bytes
    card_image_bytes = create_card(data)

    # Prepare the email components
    sender_address = os.getenv('SENDER_EMAIL')
    sender_pass = os.getenv('SENDER_PASSWORD')
    receiver_address = email
    email_subject = 'Your Card Attachment'
    email_body = f'Dear {data["first_name"]} , Please find your card attached.'

    # Create a multipart message container
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = email_subject

    # Attach the email body
    msg.attach(MIMEText(email_body, 'plain'))

    # Attach the card image as an attachment
    image_attachment = MIMEImage(card_image_bytes, name='card.png')
    msg.attach(image_attachment)

    try:
        # Create a secure SSL/TLS connection to the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_address, sender_pass)

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {str(e)}")
    finally:
        server.quit()


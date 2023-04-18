import tkinter as tk
import tkinter.filedialog as filedialog
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

email = input("Enter your email: ")
password = getpass.getpass("Enter your password: ")

# set up the SMTP server
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login(email, password)
print("Logged in")

recipient = input("Enter recipient email: ")

# create the message
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = recipient
msg['Subject'] = input("Enter subject: ")

# add body to the message
body = input("Enter message: ")
msg.attach(MIMEText(body, 'plain'))

# create a simple GUI using tkinter
print("Select image attachment")
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# attach the selected image to the message
with open(file_path, 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-Disposition', 'attachment', filename=file_path.split('/')[-1])
    msg.attach(img)

# send the message
smtp_server.sendmail(email, recipient, msg.as_string())
print("Email sent!")
# close the connection
smtp_server.quit()

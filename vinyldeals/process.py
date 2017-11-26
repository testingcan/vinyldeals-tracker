from models import Deal, Sent, session
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment
from config import sender, recipient, password

deals = session.query(Deal).filter(Deal.title.like('%.de%')).all()
sent = session.query(Sent).all()
d = []

for deal in deals:
    # Check if deal has already been sent to me
    id = session.query(Sent).filter_by(id=deal.id).first()
    if id is None:
        sent = Sent(id=deal.id)
        session.add(sent)
        session.commit()
        d.append(deal)

# Sent different mail if no new deals
if not d:
    with open("vinyldeals/mails/no_mail.jinja2") as infile:
        template = infile.read().replace("\n", "")
    mail = Environment().from_string(template).render(title = "Vinyldeals")
else:
    with open("vinyldeals/mails/mail.jinja2") as infile:
        template = infile.read().replace("\n", "")
    mail = Environment().from_string(template).render(title = "Vinyldeals", deals=d)


# Email
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)

msg = MIMEMultipart("alternative")
msg["Subject"] = "Vinyl Deals!"
msg["From"] = sender
msg["To"] = recipient

msg.attach(MIMEText(mail, "html"))

server.sendmail(sender, recipient, msg.as_string())
server.quit()

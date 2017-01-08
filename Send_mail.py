

import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
   
   
class Send_mail():
    def __init__(self, Calcul):
        self.Calcul = Calcul

    
    def message(self):
        text = """Edo de cuenta correspondiente al mes de {} {}.

                    Saludos Feliz Dia de Reyes!!
                    JaV \n\n""".format(self.Calcul.Setts.month_name,
				                 self.Calcul.Setts.this_year)
        return text
                    
    
    def email(self, passwd):
        pdffile = self.Calcul.Setts.dir_month + \
                    'Edo_{}.pdf'.format(self.Calcul.Setts.file_month)
        
        gmail_user = "jvetovazquez@gmail.com"
        to         = self.Calcul.Person_info.email
        msg = MIMEMultipart()

        msg['From'] = gmail_user
        msg['To']   = to
        msg['Subject'] = 'Edo de cuenta {}'.format(self.Calcul.Setts.month_name)

        msg.attach(MIMEText(self.message()))

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(pdffile, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(pdffile))
        msg.attach(part)

        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmail_user, passwd)
        mailServer.sendmail(gmail_user, to, msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()
        print ('Mail enviado a', to)



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
        text = """Edo de cuenta correspondiente al mes de {} 2016.

		  Debido a la alta volatilidad que han presentado los diversos
		  indices bursatiles en los ultimos meses, a la alza en las tasas
		  de intereses, a la caida del peso frente al dolar, entre muchos otros eventos,
		  la tasa de interes contemplada para las inversionde del 2017 sera del 13% anual. 
		  
		  Por otro lado, a partir del primero de Enero del 2017 existira 
		  una couta del 0.3% del monto a retirar, esto es, por cada 1,000 MXN de retiro
		  se hara un cargo de 3.0 MXN.

		  Cualquier duda, sugerencia y/o aclaracion, por este medio seran 
		  bienvenidas.

                    Saludos and Happy New Year!!
                    JaV \n\n""".format(self.Calcul.Setts.month_name)
        return text
                    
    
    def email(self, passwd):
        pdffile = self.Calcul.Setts.dir_month + \
                    'Edo_{}.pdf'.format(self.Calcul.Setts.file_month)
        
        gmail_user = "jvetovazquez@gmail.com"
        to         = self.Calcul.Person_info.email
        msg = MIMEMultipart()

        msg['From'] = gmail_user
        msg['To']   = to
        msg['Subject'] = 'Edo de cuenta {} - Recordatorio'.format(self.Calcul.Setts.month_name)

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

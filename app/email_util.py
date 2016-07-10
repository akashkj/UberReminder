"""
Utility module to send email to multiple users
"""
import logging
import smtplib

from app.app_util import ConfigurationParser


def send_email(sender_emails):
    """
    Sends email using SMTP
    :param sender_emails: list of strings email addresses of recipients
    :return: boolean success of sending email
    """
    print "sending emails to ", str(sender_emails)
    try:
        config = ConfigurationParser.get_config_object()
        config_header = "email.settings"
        smtp_server = config.get(config_header, "SMTP_SERVER")
        smtp_port = int(config.get(config_header, "SMPT_PORT"))
        email_user = config.get(config_header, "EMAIL_USER")
        email_password = config.get(config_header, "EMAIL_PASSWORD")
        email_subject = config.get(config_header, "EMAIL_SUBJECT")
        email_body = config.get(config_header, "EMAIL_BODY")
        message = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}".format(email_user, ", ".join(sender_emails), email_subject,
                                                                   email_body)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, sender_emails, message)
        server.close()
    except Exception as e:
        logging.error("{0} \nEmail was not sent to {1}".format(e, sender_emails))
        return False
    logging.info("Email sent successfully to {}".format(sender_emails))
    return True

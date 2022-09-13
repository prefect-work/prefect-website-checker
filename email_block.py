from prefect_email import EmailServerCredentials


email = EmailServerCredentials(
    username='<name>@gmail.com',
    password='<app-password>',
    smtp_server='smtp.gmail.com',
    smtp_port=465,
    smtp_type='STARTTLS',
)
email.save('<block-name>')
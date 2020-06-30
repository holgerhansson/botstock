from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(api_key):
    message = Mail(
        from_email='info@hansson.ee',
        to_emails='hansson.holger@gmail.com',
        subject='Testime',
        html_content="""testing.""")
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.body)
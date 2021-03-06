from django.core import mail
from django.test import TestCase

from weathermail.models.email import send_weathermail, Subject

class EmailTest(TestCase):

    def test_send_email(self):

        send_weathermail(Subject.GOOD, 33, "Clear", "sdfsd", "boston", "ma", "test@example.com")


        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        # Verify that the subject of the first message is correct.
        self.assertEqual(message.subject, "It's nice out! Enjoy a discount on us.")

        print message.body

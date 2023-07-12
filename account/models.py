from cryptography.fernet import Fernet
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


key = Fernet.generate_key()
cipher_suite = Fernet(key)


class EncryptedTextField(models.TextField):
    def from_db_value(self, value, expression, connection):
        """Get value from DB

        :param value: value
        :param expression: expression
        :param connection: connection
        :return: decrypted message
        """
        if value is None:
            return value
        return cipher_suite.decrypt(value.encode()).decode()

    def to_python(self, value):
        """Value Encryption

        :param value: value to encrypt
        :return: encrypted value
        """
        if not value:
            return value
        return value.encode()

    def get_prep_value(self, value):
        """Saving the encrypted value to the database

        :param value: encrypted value
        :return:  string
        """
        if not value:
            return value
        return cipher_suite.encrypt(value).decode()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = EncryptedTextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From: {self.sender.username}, To: {self.recipient.username}, Content: {self.content[:50]}"

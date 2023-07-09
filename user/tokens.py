from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.id) + str(timestamp)


email_verification_token = EmailVerificationToken()

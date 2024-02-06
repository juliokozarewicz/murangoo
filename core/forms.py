from django import forms
from django.core.mail import EmailMessage
from decouple import config
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

# log imports
from os.path import basename
import logging
from datetime import datetime
import traceback


# logs
# ---------------------------------------------------------------------------------------------
def log_generator(
    request,
    level,
    line_error,
    method_error,
    message_error
    ):
    """
    Custom Log Generator Function

    This function generates custom logs and stores them in the directory "/2_logs/webapp". It takes the following parameters:

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - level (str): The level of the log (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    - line_error (int): The line number where the error occurred.
    - method_error (str): The name of the function or method where the error occurred.
    - message_error (str): The error message or description.

    Example Usage:
    ```
    log_generator(request, 'ERROR', 42, 'handle_error', 'An error occurred while processing the request.')
    ```

    Note:
    - Logs are stored in the directory "/2_logs/webapp" with filenames indicating the date of log generation.
    - The log format includes timestamp, log level, line number, method, and error message.

    Dependencies:
    - The function relies on the existence of the "/2_logs/webapp" directory for storing log files.
    - Ensure proper file system permissions for writing logs.
    """

    # Get logger configs
    logger_webapp = logging.getLogger('webapp')

    # User configs
    # -------------------------------------------
    date_time = datetime.now()
    ip_user = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()

    if request.user.is_authenticated:
        user = request.user.email
    else:
        user = 'no_user'

    user_agent = request.META.get('HTTP_USER_AGENT', 'no_agent')

    if __package__:
        app_name = __name__.rpartition('.')[0]
    else:
        app_name = 'no_app_name'
    # -------------------------------------------

    # Log levels
    if level.lower() == 'debug':
        logger_webapp.debug(
            f'"{date_time}", '
            f'"{level}", '
            f'"{ip_user}", '
            f'"{user_agent}", '
            f'"{user}", '
            f'"{app_name}: {basename(__file__)}/{line_error}", '
            f'"{method_error}", '
            f'"{message_error}"'
        )

    elif level.lower() == 'info':
        logger_webapp.info(
            f'"{date_time}", '
            f'"{level}", '
            f'"{ip_user}", '
            f'"{user_agent}", '
            f'"{user}", '
            f'"{app_name}: {basename(__file__)}/{line_error}", '
            f'"{method_error}", '
            f'"{message_error}"'
        )

    elif level.lower() == 'warning':
        logger_webapp.warning(
            f'"{date_time}", '
            f'"{level}", '
            f'"{ip_user}", '
            f'"{user_agent}", '
            f'"{user}", '
            f'"{app_name}: {basename(__file__)}/{line_error}", '
            f'"{method_error}", '
            f'"{message_error}"'
        )

    elif level.lower() == 'error':
        logger_webapp.error(
            f'"{date_time}", '
            f'"{level}", '
            f'"{ip_user}", '
            f'"{user_agent}", '
            f'"{user}", '
            f'"{app_name}: {basename(__file__)}/{line_error}", '
            f'"{method_error}", '
            f'"{message_error}"'
        )

    elif level.lower() == 'critical':
        logger_webapp.critical(
            f'"{date_time}", '
            f'"{level}", '
            f'"{ip_user}", '
            f'"{user_agent}", '
            f'"{user}", '
            f'"{app_name}: {basename(__file__)}/{line_error}", '
            f'"{method_error}", '
            f'"{message_error}"'
        )

    else:
        logger_webapp.warning(
            f'"{date_time}", '
            f'"unrecognized", '
            f'"{ip_user}", '
            f'"{user_agent}", '
            f'"{user}", '
            f'"{app_name}: {basename(__file__)}/{line_error}", '
            f'"{method_error}", '
            f'"{message_error}"'
        )

# ---------------------------------------------------------------------------------------------


class Contact_form(forms.Form):
    """
    A Django form for handling contact information.

    This form includes fields for name, email, subject, message, and a captcha for spam prevention.
    It also contains validation logic to check for the presence of certain forbidden words in each field.

    Methods:
    - send_email(): Sends an email with the submitted contact information.
    - clean_name(): Custom validation for the name field, checking for forbidden words.
    - clean_email(): Custom validation for the email field, checking for forbidden words.
    - clean_subject(): Custom validation for the subject field, checking for forbidden words.
    - clean_message(): Custom validation for the message field, checking for forbidden words.
    - get_success_url(): Returns the success URL for redirection after form submission.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.bad_words = ['test', 'teste', 'asshole', 'fuck', 'foder', 'merda', 'test@email.com', 'test@test.com', 'bosta']

    name = forms.CharField(
        label=_('Name'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder': _('Name'),
            'class': 'name',
            'style':
                """
                """,
        }))
    
    email = forms.EmailField(
        label=_('Email'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your best email'),
            'class': 'email',
            'style':
                """
                """,
        }))

    subject = forms.CharField(
        label=_('Subject'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder': _('Subject'),
            'class': 'subject',
            'style':
                """
                """,
        }))

    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea(attrs={
            'placeholder': _('Enter your message'),
            'class': 'message',
            'style':
                """
                """,
    }))

    #captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def send_email(self):
        """
        Sends an email with the submitted contact information.

        This method uses the EmailMessage class to create and send an email to the configured recipient.
        Additionally, a copy of the email is sent to the provided email address.

        Parameters:
        None

        Returns:
        None
        """

        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        message1 = f"Name: {name.capitalize()}\nSubject: {subject.capitalize()}\nEmail: {email.lower()}\n\n\n{message.capitalize()}"

        mail = EmailMessage(
            to = [config('EMAIL_TARGET'), ],
            subject = subject.capitalize(),
            body = message1,
        )

        message_copy = f"MURANGOO | Finance:\n\n\nYour message was received:\n\n{'-' * 30}\nSubject: {subject.capitalize()}\n\n{message.capitalize()}\n{'-' * 30}\n\nWe will contact you shortly =)"

        mail_copy = EmailMessage(
            to = [email.lower(), ],
            subject = f"COPY - {subject.capitalize()}",
            body = message_copy,
        )

        mail.send()
        mail_copy.send()

    # conditions name
    def clean_name(self):
        """
        Custom validation for the name field, checking for forbidden words.

        This method cleans and validates the 'name' field by checking if it contains any forbidden words.

        Parameters:
        None

        Returns:
        str: The cleaned name value if validation is successful.
        """

        super(Contact_form, self).clean()

        name = self.cleaned_data['name'].split(' ')

        words_clean = []

        for word_clean in name:
            word_clean = word_clean.replace(',', '').replace('.', '').replace(':', '').replace('!', '').replace('"', '').replace("'", "").replace(' ', '')
            words_clean.append(word_clean)

        for word in words_clean:

            for badword in self.bad_words:

                if word.lower() == badword.lower():
                    raise ValidationError(_("Cannot contain") + f" '{word.lower()}'.")

        else:
            name = self.cleaned_data['name']
            return name

    # conditions email
    def clean_email(self):
        """
        Custom validation for the email field, checking for forbidden words.

        This method cleans and validates the 'email' field by checking if it contains any forbidden words.

        Parameters:
        None

        Returns:
        str: The cleaned email value if validation is successful.
        """

        super(Contact_form, self).clean()

        email = self.cleaned_data['email']

        for badword in self.bad_words:

            if email.lower() == badword.lower():
                raise ValidationError(_("Cannot contain") + f" '{email.lower()}'.")

        else:
            return email

    # conditions subject
    def clean_subject(self):
        """
        Custom validation for the subject field, checking for forbidden words.

        This method cleans and validates the 'subject' field by checking if it contains any forbidden words.

        Parameters:
        None

        Returns:
        str: The cleaned subject value if validation is successful.
        """

        super(Contact_form, self).clean()

        subject = self.cleaned_data['subject'].split(' ')

        words_clean = []

        for word_clean in subject:
            word_clean = word_clean.replace(',', '').replace('.', '').replace(':', '').replace('!', '').replace('"', '').replace("'", "").replace(' ', '')
            words_clean.append(word_clean)

        for word in words_clean:

            for badword in self.bad_words:

                if word.lower() == badword.lower():
                    raise ValidationError(_("Cannot contain") + f" '{word.lower()}'.")

        else:
            subject = self.cleaned_data['subject']
            return subject

    # conditions message
    def clean_message(self):
        """
        Custom validation for the message field, checking for forbidden words.

        This method cleans and validates the 'message' field by checking if it contains any forbidden words.

        Parameters:
        None

        Returns:
        str: The cleaned message value if validation is successful.
        """

        super(Contact_form, self).clean()

        message = self.cleaned_data['message'].split(' ')

        words_clean = []

        for word_clean in message:
            word_clean = word_clean.replace(',', '').replace('.', '').replace(':', '').replace('!', '').replace('"', '').replace("'", "").replace(' ', '')
            words_clean.append(word_clean)

        for word in words_clean:

            for badword in self.bad_words:

                if word.lower() == badword.lower():
                    raise ValidationError(_("Cannot contain") + f" '{word.lower()}'.")

        else:
            message = self.cleaned_data['message']
            return message

    def get_success_url(self):
        """
        Returns the success URL for redirection after form submission.

        This method is used to specify the URL to redirect to after a successful form submission.

        Parameters:
        None

        Returns:
        str: The success URL.
        """

        return reverse("/")
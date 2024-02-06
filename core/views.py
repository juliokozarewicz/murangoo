from django.shortcuts import render
from blog.models import Post
from userinfo.models import Privacy_policy
from django.views.generic import ListView, FormView, TemplateView
from .forms import Contact_form
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


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


class home(ListView):
    """
    Class (CBV) that generates the view for the home page of the institutional website.
    """

    model = Post
    template_name = 'core/home.html'

    # apply filters
    def get_context_data(self, **kwargs):
        """
        The method you can use in your view classes to add data to the context that will be passed to 
        the template. It returns a dictionary containing the context data. It is a common practice 
        to use super().get_context_data(**kwargs) to ensure that any context data defined in the 
        base class is included, and then add or modify the data as needed. This allows you to extend 
        the functionality of the base class without losing default settings.
        """

        try:
            context = super().get_context_data(**kwargs)
            context['post_last_one'] = self.get_queryset()['posts_filter_published'][0:1].get()
            context['post_last_two'] = self.get_queryset()['posts_filter_published'][1:2].get()
            context['post_last_three'] = self.get_queryset()['posts_filter_published'][2:3].get()
            return context
        
        except Exception as error:
            trace_error = traceback.extract_tb(error.__traceback__)[-1]
            line_error = trace_error.lineno
            method_error = trace_error.name
            log_generator(self.request, 'error', line_error, method_error, error)

    # filters
    def get_queryset(self):
        """
        The get_queryset method is frequently employed in Django's Class-Based Views to customize the 
        logic for retrieving objects from the database. This method is commonly found in views that 
        display lists of objects, such as ListView. By overriding the get_queryset, developers can 
        set specific criteria for the queryset, filtering or ordering objects as needed. This approach 
        provides flexibility in adjusting the default behavior of the generic view, enabling the 
        display of only the desired objects based on specific business logic.
        """

        try:
            search = {
                'posts_filter_published': Post.objects.filter(status='published').order_by('-published')
            }

            return search

        except Exception as error:
            trace_error = traceback.extract_tb(error.__traceback__)[-1]
            line_error = trace_error.lineno
            method_error = trace_error.name
            log_generator(self.request, 'error', line_error, method_error, error)

def about(request):
    """
    Function-Based View that generates the view for the 'about us' page of the institutional website.
    """

    try:
        template_name = 'core/about-us.html'
        return render(request, template_name)

    except Exception as error:
        trace_error = traceback.extract_tb(error.__traceback__)[-1]
        line_error = trace_error.lineno
        method_error = trace_error.name
        log_generator(request, 'error', line_error, method_error, error)

        template_name = 'core/about-us.html'
        return render(request, template_name)

def features(request):
    """
    Function-Based View that generates the view for the 'features' page of the institutional website.
    """

    try:
        template_name = 'core/features.html'
        return render(request, template_name)

    except Exception as error:
        trace_error = traceback.extract_tb(error.__traceback__)[-1]
        line_error = trace_error.lineno
        method_error = trace_error.name
        log_generator(request, 'error', line_error, method_error, error)
        
        template_name = 'core/features.html'
        return render(request, template_name)

class contact(FormView):
    """
    Class-Based View (CBV) that generates the view for the 'contact' page of the institutional website.
    """

    template_name = 'core/contact.html'
    form_class = Contact_form
    success_url = '/contact'

    def form_valid(self, form):
        """
        Process Form Submission and Send Email

        This method is triggered when a valid form is submitted. It performs the following actions:
        1. Calls the `send_email` method of the form, which typically handles the email sending logic.
        2. Resets the form to create a new instance, facilitating a fresh form for potential additional submissions.
        3. Adds a success message to the user indicating that their message was successfully delivered and a reply is expected.

        Parameters:
        - self: The instance of the class.
        - form: The form instance containing the submitted data.

        Returns:
        - HttpResponseRedirect: Redirects to the success URL upon successful form validation.

        Example Usage:
        ```
        def form_valid(self, form):
            # Your custom logic here, such as additional processing before or after form submission
            return super().form_valid(form)
        ```

        Note:
        - This method assumes the existence of a `send_email` method within the form class, responsible for sending emails.
        - The success message is added using Django's messages framework and can be customized as needed.
        """

        form.send_email()
        form = Contact_form()

        messages.add_message( self.request, messages.SUCCESS, _("Your message was successfully delivered! I'll reply soon =)"))

        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Handle Form Validation Failure

        This method is triggered when form validation fails. It performs the following actions:
        1. Iterates through each field in the form that has errors.
        2. Updates the HTML attributes of the corresponding form fields, adding 'id': 'red-border' to apply a red border.
        3. Calls the parent class's form_invalid method to handle the default behavior for invalid forms.

        Parameters:
        - self: The instance of the class.
        - form: The form instance containing the validation errors.

        Returns:
        - HttpResponse: The response generated by the parent class's form_invalid method.

        Example Usage:
        ```
        def form_invalid(self, form):
            # Your custom logic here, such as additional processing before or after form validation failure
            return super().form_invalid(form)
        ```

        Note:
        - This method assumes the existence of a form with HTML attributes that can be modified.
        - The 'id': 'red-border' attribute is used here as an example; customize it based on your CSS styles.
        """

        try:
            for field in form.errors:
                form.fields[field].widget.attrs.update({'id': 'red-border'})

            return super().form_invalid(form)

        except Exception as error:
            trace_error = traceback.extract_tb(error.__traceback__)[-1]
            line_error = trace_error.lineno
            method_error = trace_error.name
            log_generator(self.request, 'error', line_error, method_error, error)
            
            return super().form_invalid(form)            

class privacy_policy(TemplateView):
    """
    Class-Based View (CBV) for Displaying the Privacy Policy Page

    This view class is responsible for rendering the privacy policy page. It utilizes Django's TemplateView
    to display a template ('core/privacy_policy.html').

    Attributes:
    - template_name (str): The path to the template used for rendering the privacy policy page.

    Methods:
    - get_context_data(**kwargs): Method to add data to the context that will be passed to the template.

    Example Usage:
    ```
    privacy_view = PrivacyPolicyView.as_view()
    ```

    Note:
    - It is assumed that there is a model named `Privacy_policy` representing the privacy policy content.
    - The 'try-except' block is used to handle the case where no privacy policy object is found in the database.
    """

    template_name = 'core/privacy_policy.html'

    def get_context_data(self, **kwargs):
        """
        Get Context Data for Privacy Policy Page

        This method is used to add data to the context that will be passed to the privacy policy template.
        It returns a dictionary containing the context data. It follows the common practice of using
        super().get_context_data(**kwargs) to include any context data defined in the base class and then
        adding or modifying the data as needed.

        Parameters:
        - **kwargs: Additional keyword arguments.

        Returns:
        - dict: A dictionary containing the context data for the privacy policy template.

        Example Usage:
        ```
        context_data = self.get_context_data()
        ```

        Note:
        - If a Privacy_policy object is found in the database, it is added to the context as 'privacy_policy'.
        - If no Privacy_policy object is found, a placeholder string is added to the context.
        """

        try:
            context = super().get_context_data(**kwargs)
            context['privacy_policy'] = Privacy_policy.objects.all().last()
            
            if context['privacy_policy'] == None:
                raise Exception("Privacy Policy not found.")
        
        except Exception as error:
            trace_error = traceback.extract_tb(error.__traceback__)[-1]
            line_error = trace_error.lineno
            method_error = trace_error.name
            log_generator(self.request, 'error', line_error, method_error, error)

            context['privacy_policy'] = '...'

        return context

class service_terms(TemplateView):
    """
    Get Context Data for Privacy Policy Page

    This mixin class is used to add data to the context that will be passed to the privacy policy template.
    It follows the common practice of using super().get_context_data(**kwargs) to include any context data
    defined in the base class and then adding or modifying the data as needed.

    Parameters:
    - **kwargs: Additional keyword arguments.

    Returns:
    - dict: A dictionary containing the context data for the privacy policy template.

    Example Usage:
    ```
    class YourPrivacyPolicyView(PrivacyPolicyContextMixin, TemplateView):
        template_name = 'your_privacy_policy_template.html'

        def get_context_data(self, **kwargs):
            context_data = super().get_context_data(**kwargs)
            # Add or modify context data as needed
            return context_data
    ```

    Note:
    - If a Privacy_policy object is found in the database, it is added to the context as 'privacy_policy'.
    - If no Privacy_policy object is found, a placeholder string is added to the context.
    """

    template_name = 'core/service_terms.html'

    def get_context_data(self, **kwargs):
        """
        Override this method to provide context data for the privacy policy template.

        Returns:
        - dict: A dictionary containing the context data for the privacy policy template.
        """

        try:
            context = super().get_context_data(**kwargs)
            context['privacy_policy'] = Privacy_policy.objects.all().last()

            if context['privacy_policy'] == None:
                raise Exception("Service Terms not found.")

        except Exception as error:
            trace_error = traceback.extract_tb(error.__traceback__)[-1]
            line_error = trace_error.lineno
            method_error = trace_error.name
            log_generator(self.request, 'error', line_error, method_error, error)

            context['privacy_policy'] = '...'

        return context
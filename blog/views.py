from .models import Post
from django.views.generic import ListView, DetailView

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

class blog(ListView):
    """
    View class that lists all articles posted on the landing page blog.
    """

    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'all_post_list'

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
            context['all_post_list'] = self.get_queryset()['posts_filter_published']
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

class post_detail_content(DetailView):
    """
    View class that shows the details of articles posted on the landing page blog.
    """

    try:
        model = Post
        template_name = 'blog/post_detail.html'
        context_object_name = 'post_detail_content'

    except Exception as error:
        trace_error = traceback.extract_tb(error.__traceback__)[-1]
        line_error = trace_error.lineno
        method_error = trace_error.name
        log_generator(self.request, 'error', line_error, method_error, error)
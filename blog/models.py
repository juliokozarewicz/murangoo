from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """
    Django Model for Blog Posts

    This model represents blog posts with the following attributes:
    - title: The title of the post.
    - slug: A unique identifier for the post used in URLs.
    - author: The author of the post, represented as a foreign key to the User model.
    - content: The main content of the post.
    - cover: An image field for the post's cover image, uploaded to the 'posts/' directory.
    - published: The date and time when the post was published.
    - created: The date and time when the post was created.
    - changed: The date and time when the post was last modified.
    - status: The status of the post, with choices ('sketch', 'Sketch') and ('published', 'Published').

    Methods:
    - get_absolute_url(): Returns the absolute URL for the post detail view.

    Example Usage:
    ```
    post = Post(title='Sample Post', slug='sample-post', author=user_instance, content='Sample content...')
    post.save()
    ```

    Note:
    - Ensure that the necessary dependencies, such as the User model, are properly imported.
    - Customize the 'upload_to' path for the cover image based on your project's file structure.
    - The 'get_absolute_url' method is often used in Django templates to link to the detail view of an object.
    """

    STATUS = (
        ('sketch', 'Sketch',),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=35000)
    cover = models.ImageField(upload_to='posts/', default='')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Sketch')

    def get_absolute_url(self):
        """
        Get the absolute URL for the post detail view.

        Returns:
        - str: The absolute URL for the post detail view.
        """

        return reverse('blog:post_detail_content', args=[self.slug])

    def __str__(self):
        """
        String representation of the Post object.

        Returns:
        - str: The title of the post.
        """

        return self.title
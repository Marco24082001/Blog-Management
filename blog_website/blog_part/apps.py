from django.apps import AppConfig


class BlogPartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_part'

    def ready(self) -> None:
        import blog_part.signals

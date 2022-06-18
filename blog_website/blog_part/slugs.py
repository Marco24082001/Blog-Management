import random
import string
from django.utils.text import slugify

def generate_unique_slug(instance, base_title):
    slug = slugify(base_title)
    model = instance.__class__

    slug_exists = model.objects.filter(
        slug__exact=slug
    ).exists()
    
    while slug_exists:
        random_string = "".join(random.choices(string.ascii_lowercase, k=4))
        slug = slugify(base_title + ' ' + random_string)

        slug_exists = model.objects.filter(
            slug__exact=slug
        ).exists()

    return slug


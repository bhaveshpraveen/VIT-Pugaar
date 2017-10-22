from django.utils.text import slugify


def make_slug(department, block, floor, room=""):
    slug = "{} {} {} {}".format(department, block, floor, room)
    return slugify(slug)
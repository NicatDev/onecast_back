import random
import string


def code_slug_generator(size=5, chars=string.ascii_letters):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug_shortcode(self,size, model_):
    new_code = self.title + '-' +  code_slug_generator(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    return create_slug_shortcode(size, model_) if qs_exists else new_code
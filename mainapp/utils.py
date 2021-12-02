from mainapp.models import *


def get_model_from_slug(slug):
    if slug == 'smartfony':
        return Smartphone
    elif slug == 'noutbuki':
        return Notebook
    elif slug == 'naushniki':
        return Headphones
    else:
        return None

    # def get_model_fields(model):
    #     return model._meta.fields
    # ddd = get_model_fields(Smartphone)[2]
    # s = Smartphone.objects.get(pk=1)
    # print(getattr(s, ddd.name))


def get_product_data_for_template(model, obj):
    data = {}
    for i in model._meta.fields:
        if i.verbose_name == 'product name':
            data['product_name'] = getattr(obj, i.name)
        else:
            data[i.verbose_name] = getattr(obj, i.name)
    return data

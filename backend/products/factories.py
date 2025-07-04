import factory
from products.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)

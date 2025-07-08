import os
from django.conf import settings
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from products.models import Product
from PIL import Image
import io

class ProductImageUploadAPITest(APITestCase):
    # def test_upload_image(self):
    #     # Generate an actual image in memory
    #     image_io = io.BytesIO()
    #     image = Image.new("RGB", (100, 100), color="red")
    #     image.save(image_io, format="JPEG")
    #     image_io.seek(0)

    #     image_file = SimpleUploadedFile("test.jpg", image_io.read(), content_type="image/jpeg")

    #     url = reverse("product-list")

    #     data = {
    #         "name": "Test Product",
    #         "price": 19.99,
    #         "description": "A test product with image.",
    #         "inventory": 10,
    #         "image": image_file,
    #     }

    #     response = self.client.post(url, data, format="multipart")
    #     self.assertEqual(response.status_code, 201)
    #     self.assertTrue(Product.objects.filter(name="Test Product").exists())
        
    #     product = Product.objects.get(name="Test Product")
    #     if product.image:
    #         os.remove(os.path.join(settings.MEDIA_ROOT, product.image.name))

    # def test_upload_image_without_name(self):
    #     # Generate an actual image in memory
    #     image_io = io.BytesIO()
    #     image = Image.new("RGB", (100, 100), color="red")
    #     image.save(image_io, format="JPEG")
    #     image_io.seek(0)

    #     image_file = SimpleUploadedFile("test.jpg", image_io.read(), content_type="image/jpeg")

    #     url = reverse("product-list")

    #     data = {
    #         "price": 19.99,
    #         "description": "A test product with image.",
    #         "inventory": 10,
    #         "image": image_file,
    #     }

    #     response = self.client.post(url, data, format="multipart")
    #     self.assertEqual(response.status_code, 400)
    #     self.assertFalse(Product.objects.filter(name="Test Product").exists())
        
    def test_create_simple_product(self):
        url = reverse("product-list")
        data = {
            "name": "TestProduct",
            "description": "product for testing",
            "price": 99.5,
            "inventory": 4,
        }
        
        self.client.post(url, data)
        product = Product.objects.get(name="TestProduct")
        
        # self.assertEqual(data["name"], product.name)
        # self.assertEqual(data["description"], product.description)
        # self.assertEqual(data["price"], product.price)
        # self.assertEqual(data["inventory"], product.inventory)
        for d in data:
            self.assertEqual(data[d], getattr(product, d))
        
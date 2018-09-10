from django import test
from django.urls import reverse

print('urls >>')

client = test.Client()

# print(client.get(reverse('home')).status_code)

print('<< urls')

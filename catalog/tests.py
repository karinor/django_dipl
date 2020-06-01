from django.urls import reverse
from django.test import TestCase

# Create your tests here.
class PROBLEMA(TestCase):
    def test_printani_padla(self):
        response = self.client.get(reverse('CompareDetails'))
        self.assertTemplateUsed(response, template_name='compare.html')
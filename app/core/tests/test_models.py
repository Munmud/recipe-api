from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@munmud.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test Creating a new user with email successful"""
        email = 'test@munmud.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password), email)

    def test_new_user_email_normalized(self):
        """Test the email is normalized-2nd part is not case sensative"""
        email = 'test@MUNMUD.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test if the email is invalid or not raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test Creating a new superUser"""
        user = get_user_model().objects.create_superuser(
            'test@munmud.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingridient string representation"""
        ingridient = models.Ingridient.objects.create(
            user=sample_user(),
            name='Cucub'
        )
        self.assertEqual(str(ingridient), ingridient.name)

    def test_recipe_str(self):
        """Test the recipe strign representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mashroom sause',
            time_minute=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

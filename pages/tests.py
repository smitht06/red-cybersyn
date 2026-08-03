from django.test import TestCase
from django.urls import reverse


class HomePageViewTests(TestCase):
    """Tests for the HomePageView."""

    def test_home_page_status_code(self):
        """Test that the home page returns a 200 status code."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_by_name(self):
        """Test that the home page URL name resolves correctly."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """Test that the home page uses the correct template."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "pages/home.html")

    def test_home_page_contains_expected_content(self):
        """Test that the home page contains expected text."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Lithium")
        self.assertContains(response, "A Django starter project with batteries.")

    def test_home_page_does_not_contain_about_content(self):
        """Test that the home page does not contain about page content."""
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "About page")


class AboutPageViewTests(TestCase):
    """Tests for the AboutPageView."""

    def test_about_page_status_code(self):
        """Test that the about page returns a 200 status code."""
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_about_page_by_name(self):
        """Test that the about page URL name resolves correctly."""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_template(self):
        """Test that the about page uses the correct template."""
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "pages/about.html")

    def test_about_page_contains_expected_content(self):
        """Test that the about page contains expected text."""
        response = self.client.get(reverse("about"))
        self.assertContains(response, "About page")

    def test_about_page_does_not_contain_home_content(self):
        """Test that the about page does not contain home page content."""
        response = self.client.get(reverse("about"))
        self.assertNotContains(response, "A Django starter project with batteries.")


class PageURLTests(TestCase):
    """Tests for URL resolution."""

    def test_home_url_resolves_to_home_view(self):
        """Test that the home URL resolves correctly."""
        from pages.views import HomePageView
        from django.urls import resolve

        resolver = resolve("/")
        self.assertEqual(resolver.func.view_class, HomePageView)

    def test_about_url_resolves_to_about_view(self):
        """Test that the about URL resolves correctly."""
        from pages.views import AboutPageView
        from django.urls import resolve

        resolver = resolve("/about/")
        self.assertEqual(resolver.func.view_class, AboutPageView)

    def test_reverse_home_url(self):
        """Test that reverse('home') returns the expected URL."""
        self.assertEqual(reverse("home"), "/")

    def test_reverse_about_url(self):
        """Test that reverse('about') returns the expected URL."""
        self.assertEqual(reverse("about"), "/about/")


class AuthenticationUIVolatilityTests(TestCase):
    """
    Tests for the authentication-dependent UI in the base template.

    These tests verify that the navigation bar correctly shows
    login/signup buttons for anonymous users and settings/logout
    for authenticated users.
    """

    def test_anonymous_user_sees_login_and_signup_buttons(self):
        """Test that unauthenticated users see login and signup buttons."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Log in")
        self.assertContains(response, "Sign up")

    def test_authenticated_user_sees_settings_and_signout(self):
        """Test that authenticated users see settings dropdown and sign out."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Settings")
        self.assertContains(response, "Sign out")
        self.assertContains(response, user.email)
        self.assertNotContains(response, "Log in")
        self.assertNotContains(response, "Sign up")

from cities_light.models import City, Country
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Ingredient(models.Model):
    # Relationships
    menu_item = models.ManyToManyField("restaurants.MenuItem")

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_Ingredient_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Ingredient_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Ingredient_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Ingredient_htmx_delete", args=(self.pk,))


class Menu(models.Model):
    # Fields
    date_from = models.DateField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    date_to = models.DateField()
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_Menu_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Menu_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Menu_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Menu_htmx_delete", args=(self.pk,))


class MenuItem(models.Model):
    # Relationships
    menu = models.ForeignKey("restaurants.Menu", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_MenuItem_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_MenuItem_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_MenuItem_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_MenuItem_htmx_delete", args=(self.pk,))


class Restaurant(models.Model):
    # Relationships
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    owner = models.ManyToManyField("core.User")

    # Fields
    address = models.CharField(max_length=130)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_Restaurant_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Restaurant_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Restaurant_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Restaurant_htmx_delete", args=(self.pk,))


class Chef(User):  # type: ignore
    # Relationships
    restaurants = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.CASCADE
    )

    # Fields
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("restaurant_Chef_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Chef_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Chef_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Chef_htmx_delete", args=(self.pk,))


class Staff(User):  # type: ignore
    # Relationships
    restaurants = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.CASCADE
    )

    # Fields
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("restaurant_Staff_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Staff_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Staff_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Staff_htmx_delete", args=(self.pk,))

from django.db import models


class Person(models.Model):
    """
    Model created to store person details.
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    email_address = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    birth_date = models.DateField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="persons_on_parent",
    )

    class Meta:
        db_table = "person"

    def __str__(self):
        return self.first_name

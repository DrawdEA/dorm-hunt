from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


# Validator for rating, restricting its values to only from 1 to 5.
def validate_rating(value):
        if not (1 <= value <= 5):
            raise ValidationError("Rating must be between 1 to 5.")

# Models
class School(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100, blank=True)
    school_location = models.CharField(max_length=100)
    description = models.TextField(help_text="Describe the school and its location.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Sets a default abbreviation if not defined.
    def default_abbreviation(self):
        if not self.name:
            return ""
        abbreviated_name = self.name[0]
        for i in range(1, len(self.name)):
            if self.name[i - 1] == " ":
                abbreviated_name += self.name[i]

        return abbreviated_name

    def save(self, *args, **kwargs):
        if not self.abbreviation:
            self.abbreviation = self.default_abbreviation()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("school_detail", args=[str(self.id)])

    def __str__(self):
        return self.name

class Dorm(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="Describe the dorm and its location.")
    dorm_location = models.CharField(max_length=100)
    schools = models.ManyToManyField(School)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_school(self):
        return ", ".join(school.abbreviation for school in self.schools.all()[:10])
    
    display_school.short_description = "Schools"

    def get_absolute_url(self):
        return reverse("dorm_detail", args=[str(self.id)])

    def __str__(self):
        return self.name

class Vouch(models.Model):
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[validate_rating])
    review = models.TextField(help_text="Describe the dorm and your experience in it.")
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # Not sure na gets ko but fair enough for now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def submitted_by_name(self):
        if self.submitted_by:
            return f"{self.submitted_by.first_name} {self.submitted_by.last_name}" if self.submitted_by.first_name and self.submitted_by.last_name else self.submitted_by.username
        return None
    
    submitted_by_name.short_description = "Submitted by:"

    def get_absolute_url(self):
        return reverse("dorm_detail", args=[str(self.dorm.id)])
        
    def __str__(self):
        submitted_by_str = self.submitted_by.username if self.submitted_by else "Anonymous"
        return f"{submitted_by_str}'s Vouch: {self.dorm} - Rating: {self.rating}"




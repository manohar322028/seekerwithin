from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator



def user_image_path(instance, filename):
    return f'users/{instance.id}/images/{filename}'

def place_image_path(instance, filename):
    return f'places/{instance.place.name}/images/{filename}'

def tourist_guide_image_path(instance, filename):
    return f'tourist_guides/{instance.user.username}/images/{filename}'

def travel_package_image_path(instance, filename):
    return f'travel_packages/{instance.title}/images/{filename}'

def travel_story_image_path(instance, filename):
    return f'travel_stories/{instance.title}/images/{filename}'

class User(AbstractUser):
    profile_image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
    cover_image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
    bio = models.TextField(blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Place(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    long_description = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='administered_places')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=place_image_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.place.name} - Image {self.id}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s review of {self.place.name}"

class TouristGuide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    languages = models.CharField(max_length=255)
    contact_info = models.TextField()
    about = models.TextField()

    def __str__(self):
        return f"Guide: {self.user.username}"

class TravelPackage(models.Model):
    guide = models.ForeignKey(TouristGuide, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inclusions = models.TextField()
    exclusions = models.TextField()
    image = models.ImageField(upload_to=travel_package_image_path, null=True, blank=True)

    def __str__(self):
        return self.title

class Itinerary(models.Model):
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.package.title} - Day {self.day_number}"

class Event(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    event_type = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='forum_posts')
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s post about {self.place.name}"

class ForumReply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    reply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.post}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.place.name}"

class VisitedPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    visit_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} visited {self.place.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s booking for {self.package.title}"

class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s booking for {self.event.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content[:50]}..."

class OwnershipClaim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim for {self.place.name} by {self.user.username}"

class TravelStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=travel_story_image_path, null=True, blank=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for {self.place.name}: {self.question[:50]}..."

class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
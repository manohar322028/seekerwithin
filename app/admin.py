from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Place)
admin.site.register(PlaceImage)
admin.site.register(Review)
admin.site.register(TouristGuide)
admin.site.register(TravelPackage)
admin.site.register(Itinerary)
admin.site.register(Event)
admin.site.register(ForumPost)
admin.site.register(ForumReply)
admin.site.register(Wishlist)
admin.site.register(VisitedPlace)
admin.site.register(Booking)
admin.site.register(EventBooking)
admin.site.register(Notification)
admin.site.register(OwnershipClaim)
admin.site.register(TravelStory)
admin.site.register(FAQ)
admin.site.register(UserFollow)





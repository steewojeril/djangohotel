from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


class Dishes(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    price=models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def average_review(self):
        reviews=self.reviews_set.all()
        if reviews:
            rating=[rv.rating for rv in reviews]
            total=sum(rating)
            return total/len(reviews)
        return 0

    def total_reviews(self):
        return self.reviews_set.all().count()


class Reviews(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dishes,on_delete=models.CASCADE)
    review=models.CharField(max_length=150)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    date=models.DateField(auto_now_add=True)
    class Meta:
        unique_together=("customer","dish")
    def __str__(self):
        return self.review


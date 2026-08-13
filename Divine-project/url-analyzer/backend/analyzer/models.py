from django.db import models


class URLScan(models.Model):

    url = models.URLField()

    prediction = models.IntegerField()

    risk_score = models.FloatField()

    risk_level = models.CharField(max_length=50)

    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
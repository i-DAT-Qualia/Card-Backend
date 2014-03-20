from django.db import models


class Batch(models.Model):
    name = models.CharField(max_length=250)
    notes = models.TextField(blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    code = models.CharField(max_length=25)
    is_child = models.BooleanField(default=False)
    batch = models.ForeignKey(Batch, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.code


class Reader(models.Model):
    name = models.CharField(max_length=250)
    notes = models.TextField(blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250)
    notes = models.TextField(blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class ReaderLocation(models.Model):
    reader = models.ForeignKey(Reader)
    location = models.ForeignKey(Location)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.reader.name + " is at " + self.location.name


class Scan(models.Model):
    card = models.ForeignKey(Card)
    readerLocation = models.ForeignKey(ReaderLocation)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.card.code + " scanned at " + self.readerLocation.location.name

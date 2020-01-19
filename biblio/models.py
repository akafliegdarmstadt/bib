from django.db import models

from .utils import CopyType


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BibEntry(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    year = models.IntegerField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        authors_str = ', '.join(str(a) for a in self.authors.all())
        return '"{}". {} ({})'.format(self.title, authors_str, self.year)


class Copy(models.Model):
    copyof = models.ForeignKey(BibEntry, on_delete=models.CASCADE)
    type = models.IntegerField(choices=CopyType.choices(), default=CopyType.REAL)
    summary = models.TextField(default='', null=True, blank=True)
    file = models.FileField(help_text="Use only if type is PDF!", 
                            blank=True, null=True, upload_to='pdfs')

    def get_copy_type_label(self):
        return CopyType(self.type).name.title()

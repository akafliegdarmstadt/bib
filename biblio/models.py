from django.db import models
from django.core.exceptions import ValidationError

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
    location = models.CharField(max_length=400, default='', null=True, blank=True)
    file = models.FileField(help_text="Use only if type is PDF!", 
                            blank=True, null=True, upload_to='pdfs')

    def get_copy_type_label(self):
        return CopyType(self.type).name.title()

    def clean(self):
        if self.type in (CopyType.REAL, CopyType.SOFTWARE):
            if self.location=='' or self.location is None:
                raise ValidationError('Location muss definiert sein für diesen Typ!')
            if self.file is not None:
                raise ValidationError('Eine Datei darf für diesen Medientyp nicht angegeben werden!')
        # if type is file, file field is mandatory
        if self.type==CopyType.PDF:
            if self.file is None:
                raise ValidationError('Für diesen Medientyp muss eine Datei angegeben werden!')
            if self.location is not None and self.location!='':
                raise ValidationError('Für diesen Medientyp darf keine Location angegeben werden! {self.location}')

            

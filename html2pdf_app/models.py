from django.db import models
import uuid
# import barcode
# from barcode.writer import ImageWriter
# from io import BytesIO 
# from django.core.files import File
# Create your models here.
import qrcode
import pdfkit
# import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from barcode.ean import EAN8


class Bill(models.Model):
    employee_id = models.IntegerField()
    employee_email = models.EmailField()
    employee_name = models.CharField(max_length=100)
    job_type = models.CharField(max_length=30)
    designation = models.CharField(max_length=100)
    joindate = models.DateField(auto_now_add=False,null=True)
    date = models.DateField(auto_now_add=True,null=False)
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4,editable = False)
    # barcode = models.ImageField(upload_to='image/', blank=True)
    qrcode= models.ImageField(upload_to='qrimage/', blank=True)

    def __str__(self):
        return self.employee_name.capitalize()

    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class('ean8')
    #     #ean=EAN('5901234123457',writer=ImageWriter())
    #     ean = EAN(f'{self.employee_id}', writer=ImageWriter())
    #     buffer = BytesIO()
    #     ean.write(buffer)
    #     self.barcode.save(f'{self.employee_name}.png', File(buffer), save=False)
    #     super().save(*args, **kwargs)  
    
    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.id)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.id}.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qrcode.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs) 




 
    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class('ean13')
    #     ean = EAN(f'{self.employee_id}', writer=ImageWriter)
    #     buffer = BytesIO()
    #     ean.write(buffer)
    #     self.barcode.save('barcode.png', File(buffer), save=False)
    #     return super().save(*args, **kwargs)

    class Meta:
        ordering = ('employee_id',)


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.email


class Rejected(models.Model):
    employee_id = models.IntegerField()
    employee_email = models.EmailField()
    employee_name = models.CharField(max_length=100)
    job_type = models.CharField(max_length=30)
    designation = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True,null=False)
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4,editable = False)

    def __str__(self):
        return self.employee_name.capitalize()

    class Meta:
        ordering = ('employee_id',)


class Reexp(models.Model):
    employee_id = models.IntegerField()
    employee_email = models.EmailField()
    employee_name = models.CharField(max_length=100)
    job_type = models.CharField(max_length=30)
    designation = models.CharField(max_length=100)
    joindate = models.DateField(auto_now_add=False,null=True)
    resignationdate = models.DateField(auto_now_add=False,null=True)
    date = models.DateField(auto_now_add=True,null=False)
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4,editable = False)
    # barcode = models.ImageField(upload_to='image/', blank=True)
    qrcode= models.ImageField(upload_to='qrimage/', blank=True)


    def __str__(self):
        return self.employee_name.capitalize()

    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class('ean8')
    #     #ean=EAN('5901234123457',writer=ImageWriter())
    #     ean = EAN(f'{self.employee_id}', writer=ImageWriter())
    #     buffer = BytesIO()
    #     ean.write(buffer)
    #     self.barcode.save(f'{self.employee_name}.png', File(buffer), save=False)
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.id)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.id}.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qrcode.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs) 

  



    class Meta:
        ordering = ('employee_id',)

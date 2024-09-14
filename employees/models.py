from django.db import models
import os
from PIL import Image, ExifTags
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import io

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='employee_photos/',blank=True,null=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



    def delete(self, *args, **kwargs):
        # Delete the image file associated with the employee
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        super(Employee, self).delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        # Resizing image file to less than 300KB
        # Check if an image is uploaded
        if self.photo:
            image = Image.open(self.photo)
            image_format = image.format

            # Fix image orientation based on EXIF data
            try:
                exif = image._getexif()
                if exif is not None:
                    for orientation_tag in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation_tag] == 'Orientation':
                            break
                    else:
                        orientation_tag = None

                    if orientation_tag is not None:
                        orientation = exif.get(orientation_tag)
                        if orientation:
                            if orientation == 3:
                                image = image.rotate(180, expand=True)
                            elif orientation == 6:
                                image = image.rotate(270, expand=True)
                            elif orientation == 8:
                                image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                pass

            # Save the original image to a BytesIO object to check size
            temp_file = io.BytesIO()
            image.save(temp_file, format=image_format)
            temp_file_size_kb = temp_file.tell() / 1024  # size in KB

            # If the image size is larger than 300KB
            if temp_file_size_kb > 300:
                # Resize the image if width or height is larger than 1024px
                max_width, max_height = 1024, 1024
                if image.width > max_width or image.height > max_height:
                    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # Re-check the file size after resizing
                temp_file = io.BytesIO()
                image.save(temp_file, format=image_format)
                temp_file_size_kb = temp_file.tell() / 1024

                # If size is still larger than 300KB, reduce quality in a loop
                quality = 90  # Start with high quality
                while temp_file_size_kb > 300 and quality > 10:  # Loop until the size is <= 300KB or quality <= 10
                    temp_file = io.BytesIO()
                    image.save(temp_file, format=image_format, quality=quality)
                    temp_file_size_kb = temp_file.tell() / 1024
                    quality -= 10  # Reduce quality by 10

                # Reset the pointer in BytesIO
                temp_file.seek(0)

                # Save the compressed image to the model's photo field
                self.photo = InMemoryUploadedFile(
                    temp_file,
                    'ImageField',
                    self.photo.name,
                    f'image/{image_format.lower()}',
                    temp_file.tell(),
                    None
                )
        
        # Call the parent save method to actually save the object
        super().save(*args, **kwargs)


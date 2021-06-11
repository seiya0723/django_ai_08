from django.core.management.base import BaseCommand

from django.conf import settings
from ...models import Design

from psd_tools import PSDImage
from PIL import Image

from pdf2image import convert_from_path

import time

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        path = Design.thumbnail.field.upload_to

        while True:

            designs = Design.objects.filter(error=False,thumbnail="")
            print(designs)

            for design in designs:

                thumbnail_path = path + str(design.id) + ".png"
                full_path = settings.MEDIA_ROOT + "/" + thumbnail_path

                if design.mime == "image/vnd.adobe.photoshop":
                    image = PSDImage.open(settings.MEDIA_ROOT + "/" + str(design.file))
                    image.composite().save(full_path)
                    design.thumbnail = thumbnail_path

                elif design.mime == "application/postscript":
                    image = Image.open(settings.MEDIA_ROOT + "/" + str(design.file))
                    image.save(full_path)
                    design.thumbnail = thumbnail_path

                elif design.mime == "application/pdf":
                    images = convert_from_path(settings.MEDIA_ROOT + "/" + str(design.file))
                    images[0].save(full_path)
                    design.thumbnail = thumbnail_path

                else:

                    design.error = True

                #サムネイルのサイズを調整
                if not design.error:
                    image           = Image.open(settings.MEDIA_ROOT + "/" + str(design.thumbnail))
                    image_resize    = image.resize((250,250))
                    image_resize.save(full_path)
                    print("リサイズ")

                design.save()

            time.sleep(1)


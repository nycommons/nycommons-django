import os
import requests

from django.conf import settings
from django.core.files import File

from livinglots_usercontent.photos.models import Photo
from .refresh import UsercontentRefreshCommand


class Command(UsercontentRefreshCommand):
    help = 'Refresh photos data from LLNYC'
    local_model = Photo
    remote_site = 'llnyc'
    remote_url = settings.REMOTE_LOTS['llnyc']['api_photos_url']
    remote_object_key = 'photos'

    def download_file(self, url, pk):
        response = requests.get(url)
        local_filename = os.path.join(
            settings.MEDIA_ROOT,
            'photos',
            'remote_llnyc_%d_%s' % (pk, url.split('/')[-1])
        )
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        return local_filename

    def object_kwargs(self, file_json, orig=None):
        kwargs = super(Command, self).object_kwargs(file_json, orig=orig)
        kwargs['description'] = file_json['description']
        kwargs['name'] = file_json['name']
        if orig:
            kwargs['original_image'] = orig.original_image
        else:
            f = open(self.download_file(file_json['original_image'], file_json['pk']), 'rb')
            kwargs['original_image'] = File(f)
        return kwargs

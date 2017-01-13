import os
import requests

from django.conf import settings
from django.core.files import File as django_file

from livinglots_usercontent.files.models import File
from .refresh import UsercontentRefreshCommand


class Command(UsercontentRefreshCommand):
    help = 'Refresh files data from LLNYC'
    local_model = File
    remote_site = 'llnyc'
    remote_url = settings.REMOTE_LOTS['llnyc']['api_files_url']
    remote_object_key = 'files'

    def download_file(self, url, pk):
        response = requests.get(url)
        local_filename = os.path.join(
            settings.MEDIA_ROOT,
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
        kwargs['title'] = file_json['title']
        if orig:
            kwargs['document'] = orig.document
        else:
            f = open(self.download_file(file_json['document'], file_json['pk']), 'rb')
            kwargs['document'] = django_file(f)
        return kwargs

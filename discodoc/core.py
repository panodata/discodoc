# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import os
import shlex
import logging
import tempfile
from pprint import pprint

import requests
import subprocess

log = logging.getLogger(__name__)


class DiscodocCommand:

    def __init__(self, options):
        self.options = options
        self.headers = {}

        self.setup()

    def setup(self):
        """
        Run sanity checks and apply configuration defaults.
        """

        # Default output path.
        if self.options.output_path is None:
            self.options.output_path = os.getcwd()

        # Check output path.
        if not os.path.isdir(self.options.output_path):
            raise KeyError('Output directory "{}" does not exist'.format(self.options.output_path))

        # Discourse Api-Key for authentication.
        api_key = self.options.api_key or os.environ.get('DISCOURSE_API_KEY')
        if api_key:
            self.headers['Api-Key'] = api_key

        # Adjust renderer.
        if not self.options.renderer and self.options.format == 'pdf':
            self.options.renderer = 'latex'

    def run(self):

        # How many zeros to use when padding the filename through "--enumerate".
        enumeration_width = max(2, len(str(len(self.options.url))))

        # Acquire data and render using pandoc.
        for index, url in enumerate(self.options.url):

            # Optionally prefix filename with sequence number through "--enumerate".
            filename_prefix = None
            if self.options.enumerate:
                seqnumber = str(index + 1).rjust(enumeration_width, '0')
                filename_prefix = '{} - '.format(seqnumber)

            self.discourse_to_document(url, filename_prefix=filename_prefix)

    def discourse_to_document(self, url, filename_prefix=None):

        filename_prefix = filename_prefix or ''
        self.options.format = self.options.format or 'pdf'

        # Acquire all posts from topic.
        # Remark: The ``print=true`` option will return up to 1000 posts in a topic.
        # API Documentation: https://docs.discourse.org/#tag/Topics%2Fpaths%2F~1t~1%7Bid%7D.json%2Fget
        url = url + '.json?include_raw=true&print=true'
        response = requests.get(url, headers=self.headers)
    
        try:
            response.raise_for_status()
        except:
            log.exception('Failed requesting URL "{}". The response was:\n{}\n\n'.format(url, response.text))
            raise
    
        # Extract information.
        data = response.json()
        log.info('Collecting posts from topic #{id} "{title}" created at {created_at}'.format(**data))

        title = data['title']
        sections = []

        # Debugging
        #pprint(data)

        for post in data['post_stream']['posts']:

            if post.get('post_type') == 4:
                log.info('Skipping whisper post number {post_number}'.format(**post))
                continue

            abstract = post['raw'][:50].replace('\n', ' ')
            log.info('Collecting post number {post_number} from topic {topic_id} '
                     'created at {created_at} "{abstract}..."'.format(**post, abstract=abstract))

            sections.append(post['cooked'])
    
        # Debugging.
        #print(title); print(sections)

        # FIXME: Collect authors of all posts
        # Looks like "created_at" is actually "updated_at".
        tplvars = {'title': title, 'author': '', 'date': data['created_at'], 'pandoc_to': ''}

        # Compute output filename extension, honoring "--renderer" option.
        extension = self.options.format
        renderer = self.options.renderer
        if renderer is not None:
            # Translate into pandoc's "--to" option.
            tplvars['pandoc_to'] = '--to={}'.format(renderer)
            # Build extension.
            extension = '{}.{}'.format(renderer, extension)

        # Compute output file name.
        output_file = '{}{}.{}'.format(filename_prefix, title, extension)
        log.info('Writing standalone file "{}"'.format(output_file))

        # Compute full output path.
        if self.options.output_path is not None:
            output_file = os.path.join(self.options.output_path, output_file)

        tplvars['output_file'] = output_file

        # https://stackoverflow.com/questions/13515893/set-margin-size-when-converting-from-markdown-to-pdf-with-pandoc
        command = 'pandoc ' \
                  '--standalone --self-contained --table-of-contents ' \
                  '--from=html {pandoc_to} --resource-path=./node_modules ' \
                  '--variable=geometry:margin=2cm ' \
                  '--metadata=title="{title}" --metadata=date="{date}" --output="{output_file}"'.format(**tplvars)

        # TODO: --metadata=author="{author}"

        log.info('Invoking command: %s', command)
    
        # Write sections to temporary files.
        files = []
        filenames = []
        for section in sections:
            if not section:
                continue
            #f = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
            f = tempfile.NamedTemporaryFile()
            f.write(section.encode('utf-8'))
            f.flush()
            files.append(f)
            filenames.append(f.name)
    
        # Compute commandline arguments.
        pargs = shlex.split(command)
        pargs.extend(filenames)
    
        # Run pandoc command.
        try:
            outcome = subprocess.run(pargs, capture_output=True, timeout=60.0, check=True, encoding='utf-8')
    
        except Exception as ex:
            log.exception('Running pandoc failed, output was\nSTDOUT:\n{}\nSTDERR:\n{}\n'.format(ex.stdout, ex.stderr))
            raise

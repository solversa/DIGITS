# Copyright (c) 2015, NVIDIA CORPORATION.  All rights reserved.

import tempfile
import itertools

from . import generate_docs as _
from digits.webapp import app, _doc as doc

def check_doc_file(generator, doc_filename):
    """
    Checks that the output generated by generator matches the contents of doc_filename
    """
    with tempfile.NamedTemporaryFile(suffix='.md') as tmp_file:
        generator.generate(tmp_file.name)
        tmp_file.seek(0)
        with open(doc_filename) as doc_file:
            # memory friendly
            for doc_line, tmp_line in itertools.izip(doc_file, tmp_file):
                doc_line = doc_line.strip()
                tmp_line = tmp_line.strip()
                if doc_line.startswith('*Generated') and \
                        tmp_line.startswith('*Generated'):
                    # If the date is different, that's not a problem
                    pass
                else:
                    assert doc_line == tmp_line, '%s needs to be regenerated. Use scripts/generate_docs.py' % doc_filename

def test_api_md():
    """API.md out-of-date"""
    with app.app_context():
        generator = _.ApiDocGenerator(doc)
        check_doc_file(generator, 'docs/API.md')

def test_flask_routes_md():
    """FlaskRoutes.md out-of-date"""
    with app.app_context():
        generator = _.FlaskRoutesDocGenerator(doc)
        check_doc_file(generator, 'docs/FlaskRoutes.md')


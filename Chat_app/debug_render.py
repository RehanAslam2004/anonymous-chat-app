from app import app as flask_app
from flask import render_template

with flask_app.test_request_context('/'):
    # Try to render via Flask
    content = render_template('index.html')
    print('rendered len=', len(content))
    # Also fetch raw template source from the Jinja loader
    try:
        src, filename, upt = flask_app.jinja_loader.get_source(flask_app.jinja_env, 'index.html')
        print('loader found file:', filename)
        print('source len=', len(src))
        print('source head:', src[:400])
    except Exception as e:
        print('loader error:', e)
    # Check actual file size on disk and read raw bytes
    import os
    try:
        size = os.path.getsize(filename)
        print('os.path.getsize =', size)
        with open(filename, 'rb') as f:
            raw = f.read(400)
            print('raw bytes len=', len(raw))
            print('raw head=', raw[:200])
    except Exception as e:
        print('file read error:', e)

# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv

# load environment
load_dotenv(find_dotenv())

COV = None
if os.getenv('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from flask_script import Manager, Shell

if os.getenv('ENV').startswith('{{'):
    app = create_app('default')
else:
    app = create_app(os.getenv('ENV'))

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test(coverge=False):
    """Run the unit tests."""
    if coverage and not os.getenv('FLASK_COVERAGE'):
        import sys
        os.putenv('FLASK_COVERAGE', '1')
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    manager.run()

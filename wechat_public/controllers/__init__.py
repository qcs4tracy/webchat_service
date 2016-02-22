import os, glob
# export all controllers
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py") if not f.endswith('__init__.py')]


from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("Process_frame",  ["Process_frame.py"]),
    Extension("search",  ["search.py"]),
    Extension("model",  ["face/src/backbone/model.py"]),
    Extension("retinaface",  ["face/alignment/retinaface.py"]),
    # Extension("face_process",  ["face/face_process.py"]),
    Extension("retinaface",  ["face/alignment/retinaface_pytorch/retinaface.py"])
#   ... all your modules that need be compiled ...
]
setup(
    name = 'My Program Name',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
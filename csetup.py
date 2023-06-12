from distutils.core import Extension, setup

if __name__ == "__main__":
    c_library_dir = "CLib"
    setup(name="ctypes", version="1.0", description="Common objects to help with Melee calculations",
          ext_modules=[Extension("ctrajectory", [c_library_dir + "/ctrajectory.cpp"])])

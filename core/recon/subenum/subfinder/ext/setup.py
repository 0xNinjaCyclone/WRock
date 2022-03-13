#!/usr/bin/python3

from distutils.core import setup, Extension

def main():
    setup(name="subfinder",
          version="1.0.0",
          description="Python interface for Go subfinder project",
          author="Abdallah Mohamed",
          author_email="elsharifabdallah53@gmail.com",
          ext_modules=[
              Extension(
                  "subfinder", ["Subfinder.c"],
                  extra_compile_args = ["-pthread"],
                  extra_link_args = ["subfinder.a"]
                )
            ]
        )

if __name__ == "__main__":
    main()
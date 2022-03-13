#!/usr/bin/python3

from distutils.core import setup, Extension

def main():
    setup(name="rockrawler",
          version="1.0.0",
          description="Python interface for Go RockRawler project",
          author="Abdallah Mohamed",
          author_email="elsharifabdallah53@gmail.com",
          ext_modules=[
              Extension(
                  "rockrawler", ["crawler.c"],
                  extra_compile_args = ["-pthread"],
                  extra_link_args = ["RockRawler.a"]
                )
            ]
        )

if __name__ == "__main__":
    main()
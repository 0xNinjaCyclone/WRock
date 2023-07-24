from distutils.core import setup, Extension

def main():
    setup(name="gorock",
          version="2.0",
          description="Python interface for GoRock Framework",
          author="Abdallah Mohamed",
          author_email="elsharifabdallah53@gmail.com",
          ext_package="gorock",
          ext_modules=[
                Extension(
                    "rockrawler", ["ext/crawler.c", "ext/gorock.c"],
                    extra_link_args = ["ext/RockRawler.a"]
                ),
                Extension(
                    "subfinder", ["ext/Subfinder.c", "ext/gorock.c"],
                    extra_link_args = ["ext/subfinder.a"]
                ),
                Extension(
                    "ffuf", ["ext/fuzzer.c", "ext/gorock.c"],
                    extra_link_args = ["ext/ffuf.a"]
                )
          ])

if __name__ == "__main__":
    main()
from abc import abstractmethod


class Tag:  # TODO: Rewrite with proper HTML element class
    class HTMLConstructor:
        def __init__(self, url):
            self.url = url

            self.generated = False
            self.generatedContent = None

        @abstractmethod
        def gen(self):
            pass

    class Style(HTMLConstructor):

        def __init__(self, url, embed=False, integrity=False):
            super(url)
            self.embed = embed
            self.integrity = integrity

            if embed:
                NotImplementedError("Embedding CSS directly is no implemented yet")  # TODO

            if integrity:
                NotImplementedError("Integrity checking is not possible yet")  # TODO

        def gen(self):
            if self.generated:
                return self.generatedContent
            else:
                # TODO: Integrity check
                # TODO: Embedding into inline
                # Since the errors at the start stop the code from generating, it shouldn't be a big deal for now
                self.generatedContent = """<link rel="stylesheet" href="{}"/>""".format(self.url)
                self.generated = True
                return self.generatedContent

    class Script(HTMLConstructor):
        def __init__(self, url):
            super(url)

        def gen(self):
            if self.generated:
                return self.generatedContent
            else:
                self.generatedContent = """<script src="{}">""".format(self.url)
                self.generated = True
                return self.generatedContent
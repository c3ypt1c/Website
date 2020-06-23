from abc import abstractmethod


# TODO: Rewrite with proper HTML element class
class HTMLConstructor:
    def __init__(self, url):
        self.url = url

        self.generated = False
        self.generatedContent = None

    @abstractmethod
    def gen(self):
        pass


class Style(HTMLConstructor):
    def __init__(self, url, embed=False, integrity=False, external=False):
        super(Style, self).__init__(url)
        self.embed = embed
        self.integrity = integrity
        self.external = external

        if embed:
            NotImplementedError("Embedding CSS directly is no implemented yet")  # TODO

        if integrity and not external:
            NotImplementedError("Integrity checking for internal files is not possible yet")  # TODO

    def gen(self):
        if self.generated:
            return self.generatedContent
        else:
            # TODO: Integrity check
            # TODO: Embedding into inline
            # Since the errors at the start stop the code from generating, it shouldn't be a big deal for now

            if self.integrity and self.external:
                self.generatedContent = """<link rel="stylesheet" href="{}" integrity={} crossorigin="anonymous" />"""
                self.generatedContent = self.generatedContent.format(self.url, self.integrity)
            else:
                self.generatedContent = """<link rel="stylesheet" href="{}"/>""".format(self.url)
            self.generated = True
            return self.generatedContent


class Script(HTMLConstructor):
    def __init__(self, url):
        super(Script, self).__init__(url)
        # TODO: Script also needs integrity

    def gen(self):
        if self.generated:
            return self.generatedContent
        else:
            self.generatedContent = """<script src="{}"></script>""".format(self.url)
            self.generated = True
            return self.generatedContent

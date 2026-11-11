
from __future__ import annotations



class SoupReplacer:
    def __init__(self, og_tag=None, alt_tag=None, name_xformer=None, attrs_xformer=None, xformer=None):
        self.og_tag = og_tag
        self.alt_tag = alt_tag
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer

    def transform(self,tag):

        if self.og_tag is not None and self.alt_tag is not None:
            if tag.name == self.og_tag:
                tag.name = self.alt_tag
        if self.name_xformer is not None:
            tag.name = self.name_xformer(tag)

        if self.attrs_xformer is not None:
            tag.attrs = self.attrs_xformer(tag)

        if self.xformer is not None:
            self.xformer(tag)
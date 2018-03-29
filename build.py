#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=False)
    if os.getenv("CONAN_HEADER_ONLY", False):
        builder.builds = []
        builder.add(settings={}, options={"pugixml:header_only": True}, env_vars={}, build_requires={})

    builder.run()

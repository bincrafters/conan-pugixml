#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from bincrafters import build_template_default
from bincrafters import build_template_header_only

if __name__ == "__main__":

    builder = build_template_default.get_builder()
    if os.getenv("CONAN_HEADER_ONLY", False):
        builder = build_template_header_only.get_builder()

    builder.run()

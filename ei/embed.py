'''
Copyright (c) 2025 Yuankui Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
import inspect


def embed(resume=True, depth=0, soft_ns=None, hard_ns=None):
    # Using caller frame namespace
    frame = inspect.stack()[1 + depth].frame
    user_ns = frame.f_locals.copy()
    user_module = inspect.getmodule(frame)

    if sys.version_info < (3, 7):
        # Fix error for python<3.7
        user_ns.setdefault('__name__', user_module.__name__)

    if isinstance(soft_ns, dict):
        for key, value in soft_ns.items():
            user_ns.setdefault(key, value)

    if isinstance(hard_ns, dict):
        for key, value in hard_ns.items():
            user_ns[key] = value

    from IPython import embed
    embed(
        display_banner=False,
        user_ns=user_ns,
        user_module=user_module,
        colors=('NoColor', 'Linux')[sys.stdout.isatty()],
    )

    if not resume:
        sys.exit()

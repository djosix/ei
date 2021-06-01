'''
Copyright (c) 2021 Yuankui Lee

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
import traceback
import inspect


def embed(message=None, exit=False, color='Neutral'):
    # import IPython when function is called
    from IPython import embed

    # get exception
    e = sys.exc_info()[1]
    if e is not None and message is None:
        # set traceback message
        message = traceback.format_exc()

    # using caller frame namespace
    frame = inspect.stack()[1].frame
    user_ns = frame.f_locals
    user_module = inspect.getmodule(frame)

    if sys.version_info < (3, 7):
        # fix error in warning for python<3.7
        user_ns.setdefault('__name__', user_module.__name__)

    embed(header=message, user_ns=user_ns, user_module=user_module, colors=color)
    
    if exit:
        sys.exit()

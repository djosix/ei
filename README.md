# ei

Embedding IPython for debugging.

## Install

From GitHub:

```bash
pip install git+https://github.com.djosix/ei.git
```

From PyPI:

```bash
pip install ei
```

## Usage

`patch` and `unpatch`:

```python
def main():
    a, b, c = 1, 2, 3
    raise ValueError()

if __name__ == '__main__':
    import ei

    # replace sys.excepthook with ei.Hook(select=True),
    # refer to ei.Hook() for more options
    ei.patch(select=True)
    # set select=True if you want to choose which stack frame to embed into

    # when an exception is raised, an IPython shell will be embedded into
    # the stack frame with local variables
    main()

    # restore sys.excepthook
    ei.unpatch()
```

You can also use `capture` with the `with` statement:

```python
def main():
    a, b, c = 1, 2, 3
    raise ValueError()

if __name__ == '__main__':
    import ei

    # context manager for patch() and unpatch()
    with ei.capture(select=True):
        main()
```

In case you want to change mode and color of the traceback class:

```python
import ei

ei.probe()
'''
IPython debug hook is available!
  class ListTB
    modes: None
    colors: ['NoColor', 'Linux', 'LightBG', 'Neutral', '']
  class VerboseTB
    modes: None
    colors: ['NoColor', 'Linux', 'LightBG', 'Neutral', '']
  class FormattedTB
    modes: ['Plain', 'Context', 'Verbose', 'Minimal']
    colors: ['NoColor', 'Linux', 'LightBG', 'Neutral', '']
  class AutoFormattedTB
    modes: ['Plain', 'Context', 'Verbose', 'Minimal']
    colors: ['NoColor', 'Linux', 'LightBG', 'Neutral', '']
  class ColorTB
    modes: ['Plain', 'Context', 'Verbose', 'Minimal']
    colors: ['NoColor', 'Linux', 'LightBG', 'Neutral', '']
  class SyntaxTB
    modes: None
    colors: ['NoColor', 'Linux', 'LightBG', 'Neutral', '']
'''

# default: AutoFormattedTB
ei.patch(tb_mode='Verbose', tb_color='Linux')

def fuckup(n):
    n = 123 / n
    return n

print(fuckup(0))
```

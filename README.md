# ei

Automatically embed IPython into arbitrary stack frames in traceback.

[![asciicast](https://asciinema.org/a/jWSj75lwjHfxUmtkSyWRGN2Tx.svg)](https://asciinema.org/a/jWSj75lwjHfxUmtkSyWRGN2Tx)

## Install

```bash
# PyPI
pip3 install ei

# GitHub
pip3 install git+https://github.com.djosix/ei.git
```

## Usage

Basic usage:

```python
def main():
    a = 123
    b = 0
    return a / b

if __name__ == '__main__':
    import ei
    ei.patch() # overwrites sys.excepthook

    main()
```

Unpatch to recover `sys.excepthook`:

```python
ei.unpatch()
```

Context manager:

```python
with ei.capture():
    main()

# The exception hook is recovered here
```

Lazy patch:

```python
import ei.patched
```

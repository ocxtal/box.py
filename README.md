# box.py

migrated from [https://bitbucket.org/suzukihajime/box](https://bitbucket.org/suzukihajime/box)

Box.py generates outlines of the six surfaces of a cube with configuarable board thickness and cog pitch, making it easy to assemble boxes with wood and plastics using laser cutting machines.

![img](https://github.com/ocxtal/box.py/blob/master/cube.png)

## Dependency

Python 2.7+ or 3.3+ with [dxfwrite](https://pypi.python.org/pypi/dxfwrite/) installed.


## Usage

```
./box.py <width> <height> <depth> -t<thickness> -p<pitch> > out.dxf
```

## License

MIT

Copyright (c) 2015-2016 Hajime Suzuki
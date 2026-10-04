This code is cited in the pyboolnet Manual.

Espresso is required for heuristic minimization Boolean expressions. For more information see

* http://chmod755.tumblr.com/post/31417234230/espresso-heuristic-logic-minimizer

The `espresso-modern.tar.gz` has been downloaded here for reference.

UC Berkeley, Espresso Version #2.3, Release date 01/31/88

## Install for the current user

The original `INSTALL` builds as root and copies the binary and man pages into system directories. 

To install into your home directory `~/bin` instead, run the same build from this directory like so:

```bash
tar xzvf espresso-modern.tar.gz
cd espresso/espresso/source
chmod +x configure
./configure --bindir="$HOME/bin" CFLAGS="-g -O2 -std=gnu89"
make clean
make
make install
mkdir -p "$HOME/bin/manual"
cp ../manpages/espresso.1 "$HOME/bin/manual/"
cp ../manpages/espresso.5 "$HOME/bin/manual/"
```

The tarball already contains object files and an `espresso` binary. Their timestamps are newer than the sources, so a plain `make` reports nothing to do. `make clean` removes them so the sources are compiled. `-std=gnu89` is required because `unate.c` uses `restrict` as a variable name, and current gcc treats that as a keyword.

That places the `espresso` executable in `~/bin` and the man pages in `~/bin/manual`. Add `~/bin` to `PATH` and `~/bin/manual` to `MANPATH` if they are not already there.


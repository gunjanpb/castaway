# `$ castaway`

Discovers [dotfiles](https://github.com/webpro/awesome-dotfiles) that are not being tracked in any of your [homeshick](https://github.com/andsens/homeshick) castles. Think of it as `chezmoi unmanaged` equivalent for homeshick / [homesick](https://github.com/technicalpickles/homesick).


## Installation

```sh
mise use -g pypi:gunjanpb/castaway
```
or
```sh
pipx install git+https://github.com/gunjanpb/castaway.git
```

### Upgrading
```sh
mise install --force pypi:gunjanpb/castaway
```

## Usage

```sh
castaway
```

scans your `$XDG_CONFIG_HOME` (which is usually `~/.config`) and prints newline-separated file paths that are not tracked in any castle.

## Configuration

### Ignoring paths
 
`$XDG_CONFIG_HOME/castaway.ignore` has gitignore-styled paths that it ignores. The file will be created if it does not exist.

If you made any changes to the ignore list, you may want to track them in your own castle, e.g. if your castle name is dotfiles,
```bash
homeshick track dotfiles $XDG_CONFIG_HOME/castaway.ignore
```
It is encouraged to also submit such changes here.

### Scan depth

castaway ignores files too deep in hierarchy (3 levels, by default). To control:
```bash
CASTAWAY_MAX_DEPTH=5 castaway
```

## Development

```sh
flit install --symlink
```
makes your local changes available as `castaway` on command-line.

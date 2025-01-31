# CFEngine Hackaton

To build debian packages you need:
- build-essential
- devscripts
- debhelper

## Roadmap
- Support platforms other than only Debian. This will require adding a
  `--platform` argument that defines different contexts to the [context
  dictionary](#context-dictionary) based on the platform.
- Command to generate release information table as markdown. Add optional
  `"comment"` field to [deps-packaging.json](#deps-packagingjson) which will be
  included in the table.
- Command to automatically update dependencies in
  [deps-packaging.json](#deps-packagingjson). Use [Release
  Monitoring](https://release-monitoring.org/) to determine if there is a new
  release available. We may need to add a `"release-monitoring"` field
  [deps-packaging.json](#deps-packagingjson).

## Context dictionary

Different contexts are created based on the command-line arguments passed to the
program. The context is stored as a dictionary. E.g., if you specify
`--project=enterprise` as a command-line argument, then the context will contain
at least:

```python
{
    "any": True,
    "enterprise": True,
    "community": False,
    ...
}
```

Let's try to maintain a complete list of all possible contexts here:

| Context        | `True` if (otherwise `False`) |
|----------------|-------------------------------|
| `"any"`        | Always `True`                 |
| `"agent"`      | `--role=agent`                |
| `"hub"`        | `--role=hub`                  |
| `"enterprise"` | `--project=enterprise`        |
| `"community"`  | `--project=community`         |
| `"release"`    | `--build-type=release`        |
| `"debug"`      | `--build-type=debug`          |

## deps-packaging.json

Dependencies to be packaged with CFEngine are listed in
[deps-packaging.json](deps-packaging.json). The packages will be built in the
order they appear.

The `"expression"` field is passed to `eval()` along with the [context
dictionary](#context-dictionary). The outcome of `eval() determines whether or
not the dependency will be built.

The packages are fetched by concatenating the `"source"` and the `"tarball"`
field and will be stored in the `build/tarballs` directory.

The fetched tarball is computed into a SHA-256 digest which is compared to the
`"checksum"` field to ensure integrity.

The `"version"` field is used as the upstream version and `-1` will be appended
as the Debian package version when packaging the dependency.

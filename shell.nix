{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  buildInputs = [
    librime

    stdenv.cc
    pkg-config

    (python3.withPackages (
      p: with p; [
        uv
        pytest

        meson-python
        cython
        autopxd2
      ]
    ))
  ];
}

{ pkgs ? import <nixpkgs> { } }:

with pkgs;
mkShell {
  name = "zsh";
  buildInputs = [
    meson
    ninja
    pkg-config
    librime
    stdenv.cc
  ];
}

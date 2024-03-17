{ pkgs }: {
  deps = [
    pkgs.gnupg1orig
    pkgs.gtg
    pkgs.apg
    pkgs.vim
    pkgs.sqlite.bin
  ];
}
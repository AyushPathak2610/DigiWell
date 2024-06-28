{pkgs}: {
  deps = [
    pkgs.espeak-ng
    pkgs.pkg-config
    pkgs.arrow-cpp
    pkgs.libsndfile
    pkgs.ffmpeg-full
  ];
}

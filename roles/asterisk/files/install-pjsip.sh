PJPROJECT_VERSION=2.5.5
PJPROJECT_URL=http://www.pjsip.org/release/${PJPROJECT_VERSION}/pjproject-${PJPROJECT_VERSION}.tar.bz2

if [ ! -f /usr/lib/libpj.so ]; then
  if [ ! -d pjproject-${PJPROJECT_VERSION} ]; then
    curl -s $PJPROJECT_URL | tar -xj
  fi

  cd pjproject-${PJPROJECT_VERSION}
  ./configure --prefix=/usr \
              --enable-shared \
              --disable-sound \
              --disable-resample \
              --disable-video \
              --disable-opencore-amr \
              CFLAGS='-O2 -DNDEBUG'

  make dep
  make
  sudo make install
  sudo ldconfig
  cd ..
fi

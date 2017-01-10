ASTERISK_VERSION=13.13.1
ASTERISK_URL=http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-${ASTERISK_VERSION}.tar.gz

if [ ! -f /etc/init.d/asterisk ]; then
  if [ ! -d asterisk-${ASTERISK_VERSION} ]; then
    mkdir asterisk-${ASTERISK_VERSION}
    curl -s $ASTERISK_URL | tar -xvz --strip-components=1 -C asterisk-${ASTERISK_VERSION}
  fi

  cd asterisk-${ASTERISK_VERSION}
  ./configure
  make menuselect.makeopts
  make
  make config
  make install

  cd ..
fi

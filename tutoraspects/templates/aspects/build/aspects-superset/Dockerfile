# Superset image with additional database drivers
# https://hub.docker.com/r/apache/superset
# https://github.com/apache/superset/releases
# https://github.com/apache/superset/blob/master/Dockerfile
# https://superset.apache.org/docs/databases/installing-database-drivers
FROM apache/superset:2.1.0

USER root

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

# Extracted from https://superset.apache.org/docs/installation/alerts-reports/#custom-dockerfile
ARG GECKODRIVER_VERSION=v0.32.0
ARG FIREFOX_VERSION=106.0.3

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
          libnss3 \
          libdbus-glib-1-2 \
          libgtk-3-0 \
          libx11-xcb1 \
          libasound2 \
          libxtst6 \
          wget

# Install GeckoDriver WebDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar xvfz /tmp/geckodriver.tar.gz -C /tmp && \
    mv /tmp/geckodriver /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Install Firefox
RUN wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2 -O /opt/firefox.tar.bz2 && \
    tar xvf /opt/firefox.tar.bz2 -C /opt && \
    ln -s /opt/firefox/firefox /usr/local/bin/firefox

USER superset

FROM ubuntu:bionic

# This Dockerfile adds a non-root user with sudo access. Use the "remoteUser" property in
# devcontainer.json to use it. More info: https://aka.ms/vscode-remote/containers/non-root-user.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# Other options for common setup script
ARG INSTALL_ZSH="true"
ARG UPGRADE_PACKAGES="false"
ARG COMMON_SCRIPT_SOURCE="https://raw.githubusercontent.com/microsoft/vscode-dev-containers/master/script-library/common-debian.sh"
ARG COMMON_SCRIPT_SHA="dev-mode"

# Java
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Scala
ENV SCALA_VERSION 2.11.12
ENV SCALA_PACKAGE scala-${SCALA_VERSION}.deb

# Hadoop
ENV HADOOP_VERSION 2.7.3
ENV HADOOP_HOME /usr/local/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop
ENV HADOOP_OPTS ${HADOOP_OPTS} -Djava.library.path=${HADOOP_HOME}/lib/native
ENV HADOOP_COMMON_LIB_NATIVE_DIR ${HADOOP_HOME}/lib/native/
ENV PATH $PATH:$HADOOP_HOME/bin

# SPARK
ENV SPARK_VERSION 2.4.6
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-hadoop2.7
ENV SPARK_HOME /usr/local/spark-${SPARK_VERSION}
ENV CLASSPATH ${CLASSPATH}:${HADOOP_HOME}/lib/*
ENV PYTHONPATH ${SPARK_HOME}/python/:${PYTHONPATH}
ENV PATH $PATH:${SPARK_HOME}/bin:$SPARK_HOME/sbin
ENV PYSPARK_PYTHON /usr/bin/python

# Install needed packages and setup non-root user. Use a separate RUN statement to add your own dependencies.
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends curl ca-certificates 2>&1 \
    && curl -sSL  ${COMMON_SCRIPT_SOURCE} -o /tmp/common-setup.sh \
    && ([ "${COMMON_SCRIPT_SHA}" = "dev-mode" ] || (echo "${COMMON_SCRIPT_SHA} */tmp/common-setup.sh" | sha256sum -c -)) \
    && /bin/bash /tmp/common-setup.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" \
    && rm /tmp/common-setup.sh \
    # Python/Java install
    && apt-get -y install software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get -y install openjdk-8-jdk python3.7 python3-pip procps hostname \
    && ln -s /usr/bin/python3.7 /usr/bin/python \
    # Scala install
    && curl -s --retry 3 \
        "https://downloads.lightbend.com/scala/${SCALA_VERSION}/${SCALA_PACKAGE}" -o "${SCALA_PACKAGE}" \
    && dpkg -i "./${SCALA_PACKAGE}" \
    && rm "${SCALA_PACKAGE}" \
    # Spark install
    && curl -s --retry 3 \
        "https://downloads.apache.org/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \ 
        | gunzip \
        | tar x -C /usr/local \
    && mv "/usr/local/${SPARK_PACKAGE}" "${SPARK_HOME}" \
    && chown -R root:root "${SPARK_HOME}" \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# [Optional] Uncomment this section to install additional OS packages you may want.
#
# RUN apt-get update \
#     && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

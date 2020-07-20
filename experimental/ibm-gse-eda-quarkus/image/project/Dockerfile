## Stage 1 : build with maven builder image jvm capabilities
FROM quay.io/quarkus/centos-quarkus-maven:19.3.1-java11 AS build

COPY . /project
RUN cd /project && mvn -B install dependency:go-offline -DskipTests
# Install user-app dependencies
WORKDIR /project/user-app
COPY ./user-app/src ./src
COPY ./user-app/pom.xml ./
USER root
RUN chown -R quarkus .
USER quarkus
RUN mvn -B clean package


## Stage 2 : create the docker final image
FROM registry.access.redhat.com/ubi8/ubi-minimal:8.1

ARG JAVA_PACKAGE=java-11-openjdk-headless
ARG RUN_JAVA_VERSION=1.3.8

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en'

# Install java and the run-java script
# Also set up permissions for user `1001`
RUN microdnf install curl ca-certificates ${JAVA_PACKAGE} \
    && microdnf update \
    && microdnf clean all \
    && mkdir /deployments \
    && chown 1001 /deployments \
    && chmod "g+rwX" /deployments \
    && chown 1001:root /deployments \
    && curl https://repo1.maven.org/maven2/io/fabric8/run-java-sh/${RUN_JAVA_VERSION}/run-java-sh-${RUN_JAVA_VERSION}-sh.sh -o /deployments/run-java.sh \
    && chown 1001 /deployments/run-java.sh \
    && chmod 540 /deployments/run-java.sh \
    && echo "securerandom.source=file:/dev/urandom" >> /etc/alternatives/jre/lib/security/java.security

# Configure the JAVA_OPTIONS, you can add -XshowSettings:vm to also display the heap size.
ENV JAVA_OPTIONS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"

COPY  --from=build /project/user-app/target/lib/* /deployments/lib/
COPY --from=build /project/user-app/target/*-runner.jar /deployments/app.jar
#COPY --from=build /project/user-app/certs/server.truststore /deployments/server.truststore 

EXPOSE 8080
USER 1001

ENTRYPOINT [ "/deployments/run-java.sh" ]


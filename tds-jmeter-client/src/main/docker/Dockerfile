FROM hhcordero/docker-jmeter-client:latest

ADD loadtest-library-*.jar /usr/local/apache-jmeter-2.13/lib/loadtest-library.jar
ADD user.properties /usr/local/apache-jmeter-2.13/bin/user.properties
ADD hc.parameters /usr/local/apache-jmeter-2.13/bin/hc.parameters

WORKDIR /usr/local/apache-jmeter-2.13/bin

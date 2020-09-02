# Kakfa template for Quarkus

This template provides a Java application which demonstrates using MicroProfile Reactive Messaging to consume and produce messages on Kafka topics. The application uses the example from the [Quarkus Kafka guide](https://quarkus.io/guides/kafka). 

A bean produces a random `Integer` onto a Reactive Messaging channel named "generated-price" every 5 seconds. This channel is connected to a Kafka topic named "prices". Another bean consumes from that topic, applies a conversion, and publishes a `double` onto another channel named "my-data-stream". Finally, that channel is streamed to a JAX-RS endpoint `/prices.html`, using [Server-sent Events](https://en.wikipedia.org/wiki/Server-sent_events).


## Running locally

The template provides a sample `docker-compose.yaml` which you can use to run a single-node Kafka cluster on your local machine. To start Kafka locally, run `docker-compose up`. This will start Kafka, Zookeeper, and also create a Docker network (kafkanet) on your machine, which you can find the name of by running `docker network list`.

To run the application using Appsody, use the following command, substituting in the name of your Docker network if needed:

```shell
$ appsody run --network kafkanet --docker-options "--env KAFKA_BROKERS=kafka:9092"
```

Use the web browser to access [http://localhost:8080/prices.html](http://localhost:8080/prices.html) to see a stream of price sent to the web browser.

To shutdown Kafka and Zookeeper afterwards, run `docker-compose down`.

## Running locally with remote Event Streams

You need to have a running Event Streams instance on OpenShift cluster. Then proceed to do the following steps:

* Login to OpenShift with oc CLI and connect to an the project where event streams is installed:

```shell
oc login --server=... --token=...
oc project eventstreams
```

* connect to an existing project or create a new project:

```
cloudctl es init
# select the target instance, in case you have multiple Event Streams cluster.
```

Get the `Event Streams bootstrap address`.

* Rename `scripts/appsody-templ.env` to `scripts/appsody.env`, and define the KAFKA_BROKERS env variable in this file using the bootstrap address specified in previous step.


* Select one of the kafka users defined or create a new one with the produce, consume messages and create topic and schemas authorizations, on all topics or topic with a specific prefix, on all consumer groups or again with a specific prefix, all transaction IDs.

```shell
oc get kafkausers -n eventstreams
```

 Get username and then to get the password do the following:

 ```shell
oc get secret <username>  -o jsonpath='{.data.password}' | base64 --decode
 ```

Modify the KAFKA_USER and KAFKA_PASSWORD variables in the `scripts/appsody.env` file.

* Then get the TLS certificate with the command:

```shell
cloudctl es certificates --format p12
# get the truststore password
# mv the certificate
mv es-cert.p12 certs
```

The cluster Truststore certificate is required for all external connections and is available to download from the Cluster connection panel under the Certificates heading. Upon downloading the PKCS12 certificate, the certificate password will also be displayed.

Modify KAFKA_CERT_PWD in the `scripts/appsody.env` file.

* Remove the "%prod." in the application.properties for the kafka settings. These were set to run with Kafka running with docker compose, but when remote connected to Event Streams we need those settings.

* Start appsody with the environment variables.

```shell
appsody run --docker-options "--env-file ./scripts/appsody.env -v $(pwd)/certs:/deployment/certs"
```


## Running on OpenShift with Event Streams

To run on OpenShift, you will need to inject the address of your Kafka settings into your Quarkus application via the environment variables and mount point. The `app-deploy.yaml` file contains declarations to inject those data at runtime. 
We just need to add config maps and secrets to the project where we want to deploy this app.

* Modify the `src/main/kubernetes/configmap.yaml` by replacing the user and broker data with the matching user and bootstrap server external URL. We have to use the external URL as the app is not deployed in the same cluster as Event Streams. See next section if you deploy on the same cluster and want to use the internal URL. 

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-brokers
data:
  user: <kafka-username>
  brokers: <broker-bootstrap-url>
```

Then do: `oc apply -f src/main/kubernetes/configmap.yaml`

* Move secret for user password from the Event Streams project to the target project. Here is an example of such command: 

```shell
oc get secret jesus -n eventstreams --export -o yaml | oc apply -n sandbox -f -
```

* Get the cluster public certificate <>-cluster-ca-cert secret from the Event Streams project to the target project. This certificate includes a ca.pa12 entry and a truststore password which will be used in the deployment manifest.

```
oc get secret minimal-prod-cluster-ca-cert -n eventstreams --export -o yaml | oc apply -n jbsandbox -f -
```

Here is an example of content:

```
Name:         minimal-prod-cluster-ca-cert
Namespace:    jbsandbox
Labels:       app.kubernetes.io/instance=minimal-prod
              app.kubernetes.io/managed-by=eventstreams-cluster-operator
              app.kubernetes.io/name=eventstreams
              app.kubernetes.io/part-of=eventstreams-minimal-prod
              eventstreams.ibm.com/cluster=minimal-prod
              eventstreams.ibm.com/kind=Kafka
              eventstreams.ibm.com/name=eventstreams
Annotations:  eventstreams.ibm.com/ca-cert-generation=0

Type:  Opaque

Data
====
ca.crt:       1164 bytes
ca.p12:       1114 bytes
ca.password:  12 bytes
```

* Modify the secret name in the volume declaration. The mountPath and subPath need to match the data key 'ca.p12'. 

```yaml
  volumeMounts:
  - mountPath: /deployments/certs/ca.p12
    name: es-cert
    readOnly: true
    subPath: ca.p12
  volumes:
  - name: es-cert
    secret:
      secretName: minimal-prod-cluster-ca-cert

```

* Deploy the application via: 

```shell
appsody deploy -t <registry>/<imagename>:<tag> --push --namespace <targetproject>
```

* The app is exposed as to the external world via a route. `oc get routes`, so the web socket connection to get the price changes from kafka is at http://<routes>/prices.html.

If you want to remove the deployment:

`oc delete app-deploy.yaml`

## Run on same cluster

So to use the internal URL for the bootstrap server, do the following:

* use the short URL for the broker in the `src/main/kubernetes/configmap.yaml`.
* 

## Common errors

* unable to find valid certification path to requested target: wrong certificate match between the client truststore which includes the public server certificate, and the certificate received while connecting.

* Metadata update failed due to authentication error: org.apache.kafka.common.errors.SslAuthenticationException: SSL handshake failed. SSL handshake failures in clients may indicate client authentication failure due to untrusted certificates if server is configured to request client certificates. Handshake failures could also indicate misconfigured security including protocol/cipher suite mismatch, server certificate authentication failure or server host name verification failure.
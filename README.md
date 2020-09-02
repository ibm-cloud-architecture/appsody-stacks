# IBM Cloud Architecture Appsody incubator stacks


## To get access to those stacks

Add a new repository into your local environment by using the command

```shell
appsody repo add ibmcase https://raw.githubusercontent.com/ibm-cloud-architecture/appsody-stacks/master/ibmcase-index.yaml

# Verify the repository 
appsody list
# you should see template like
REPO        	ID                            	VERSION  	TEMPLATES               	DESCRIPTION  
ibmcase     	ibm-gse-eda-quarkus           	1.7.1    	default, *kafka         	Quarkus ... runtime for running Java applications     
```

## Create a project

* For Kafka Quarkus reactive messaging basic: `appsody init ibmcase/ibm-gse-eda-quarkus`
* Quarkus basic: `appsody init ibmcase/ibm-gse-eda-quarkus default` 

## Update an existing stack

Update the code in the experimental folder, and update templates content or add new template.

Typical update: pom.xml, image/config/app-config.yaml...

Package the stack to get it in the local repository

```
 appsody stack package --image-namespace ibmcase

 appsody list
```

Test your stack scaffold

```shell
$ appsody init dev.local/ibm-gse-eda-quarkus kafka
```

Once done, package your stack to create a docker images that will be pushed to dockerhub registry

```shell
appsody stack package --image-namespace ibmcase --image-registry docker.io
docker push ibmcase/ibm-gse-eda-quarkus 
```

Add a new git release in this repo. For example with tag 1.7.1. [See this documentation for detail](https://docs.github.com/en/enterprise/2.13/user/articles/creating-releases).

* Redefined the repository index, so from the source of all the stacks do

```shell
appsody stack add-to-repo ibmcase --release-url https://github.com/ibm-cloud-architecture/appsody-stacks/releases/download/1.7.1/
# this command updates the following files
ibmcase-index.json
ibmcase-index.yaml
```
* copy those file into root folder of the stack project

* Upload the source code and template archives to the release using drag and drop. The files are

```shell
ibm-gse-eda-quarkus.v1.7.1.source.tar.gz
ibm-gse-eda-quarkus.v1.7.1.templates.default.tar.gz
ibm-gse-eda-quarkus.v1.7.1.templates.kafka.tar.gz
ibmcase-index.json
ibmcase-index.yaml
```

then publish the release which can be see at the URL: [https://github.com/ibm-cloud-architecture/appsody-stacks/releases](https://github.com/ibm-cloud-architecture/appsody-stacks/releases).
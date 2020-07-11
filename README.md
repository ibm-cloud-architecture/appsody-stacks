# IBM Cloud Architecture Appsody incubator stacks


## To get access to those stacks

Add a new repository into your local environment by using the command

```shell
appsody repo add ibmcase https://raw.githubusercontent.com/ibm-cloud-architecture/appsody-stacks/master/ibmcase-index.yaml

# Verify the repository 
appsody list
# you should see template like
REPO        	ID                            	VERSION  	TEMPLATES               	DESCRIPTION  
ibmcase     	ibm-gse-eda-quarkus           	0.4.1    	default, *kafka         	Quarkus 1.5.3 runtime for running Java applications     
```

## Create a project

* For Kafka quarkus reactive messaging basic: `appsody init ibmcase/ibm-gse-eda-quarkus`
* Quarkus basic: `appsody init ibmcase/ibm-gse-eda-quarkus default` 

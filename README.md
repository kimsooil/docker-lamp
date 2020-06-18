# Getting Started
This is DJANGO dockerized application for displaying COVID-19 projections.

In order to begin using this repository, along with any other migrations that involve user groups, you will immediately need to run the manage.py addhashes --all to download all the current datahashes used for the model. Without these, the model will not run. The command is outlined further below.

## The covid folder contains 4 main DJANGO Models for the projections:
1. State
2. County
3. SimulationRun
4. HashValue

### SimulationRun

Simulation Run is designed to create the the DJANGO object stored in the database, get status updates for the simulation and handle webhooks, and ensure that the same job regarless of where it has been run will return results efficiently.

Users are split into 1 of 3 groups (which correspond to where the model will be ran). If the following groups are not created prior to running the model, the model will always be run using the Fargate Resource.
- Fargate
- Fargate Spot
- Onboard

The ModelRunner handles starting any of the jobs on any of the 3 resources. 

#### Fargate:
  - The model runner will compile an object (model inputs) to be uploaded to AWS S3
  - This immediately triggers an AWS Lambda function which reads the S3 created object and connects to AWS ECS to begin                    running a task in our ECS Cluster with environmnet variables (model inputs) obtained from the s3 object
  - This task is connected to an AWS ECR container which immediately begins to run the model projection
  - This container will continuously send updates for the model through a webhook until the job has completed.
  
#### Fargate Spot (similar to FARGATE):
  - The model runner will compile an object (model inputs) to be uploaded to AWS S3
  - This immediately triggers an AWS Lambda function which reads the S3 created object and connects to AWS ECS to begin                    running a task in our ECS Cluster with environmnet variables (model inputs) obtained from the s3 object
  - This task is connected to an AWS ECR container which immediately begins to run the model projection
  - This container will NOT send updates back to the user until the model is completed running.
  - As FArgate Spot is run on AWS's excess resources, AWS may terminate the resource at any time. 
  - IN THE CASE OF TERMINATION:
    - A CloudWatch event rule is trigged using EventBridge which triggers a separate Lambda function
    - This Lambda Functiion will then trigger another ECS task to run a new container when AWS has avaialble resources with the same envrionment variables from the first container
    
#### Onboard Compute
  - The model runner will send a request to a flask api with the model inputs to a flask api to start the projection
  - The model runner will send new requests to the flask api to receive status updates for the model, once it has been verified as a running or completed model
 
### HashValue
All 3 of these simulation run resources depend on a data hash which is updated daily via github. The data hash can be updated using a manage.py command - addhashes. The model default is to use the most recent hash in the database, if the addhashes --all is not run prior to using this repository, it will fail every time.

  - manage.py addhashes
      - adds any new data hashes to the database until it finds a hash that is present in the database
      - used to update the database with daily hashes when a database is already populated with hashes
  - manage.py addhashes --all
      - adds every data hash available on github to the database
      - used the very first time the database is populated or after you have deleted all data hashes
  - manage.py addhashes --delete
      - deletes all hash values stored in the database
      - to be used if there is an error with the data hashes currently stored in the databse
      
## For more information

All of the information for the model output from the Fargate and Fargate Spot resources as well as the Lambda functions are logged via CloudWatch logs.

To learn more about AWS Fargate: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html

To learn more about AWS Fargate Spot: https://aws.amazon.com/blogs/aws/aws-fargate-spot-now-generally-available/

To learn more about entire system setup (S3 -> lambda -> ECS): https://www.serverless.com/blog/serverless-application-for-long-running-process-fargate-lambda/

 

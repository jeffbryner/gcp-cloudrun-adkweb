# GCP-CloudRun-adkweb

Simple cloud run hosted AI agent using the google agent development kit and the adk web interface.
Based on this starter kickstarter project : https://github.com/jeffbryner/gcp-project-pipeline

## Why?

This is meant to simply satisfy the urge to dream up an AI agent, give it a name and location in the org tree, terraform apply and then immediately begin using the ci/cd pipeline to build the remaining infrastructure.

## Setup
You will need to be able to create a project with billing in the appropriate place in your particular org structure. First you'll run terraform locallly to initialize the project and the pipeline. After the project is created, we will transfer terraform state to the cloud bucket and from then on you can use git commits to trigger terraform changes without any local resources or permissions.

1. Clone this repo

2. Change directory (cd) to the cicd directory and edit the terraform.tfvars to match your GCP organization.

3. Run the following commands in the cicd directory to enable the necessary APIs,
   grant the Cloud Build service account the necessary permissions, and create
   Cloud Build triggers and the terraform state bucket:

    ```shell
    terraform init
    terraform apply
    ```
4. Get the name of the terraform state bucket from the terraform output

    ```shell
    terraform output
    ```
  and copy backend.tf.example as backend.tf with the proper bucket name.

    ```terraform
        terraform {
      backend "gcs" {
        bucket = "UPDATE_ME_WITH_OUTPUT_OF_INITIAL_INIT"
        prefix = "cicd"
      }
    }
    ```

  Note that if you create other directories for other terraform concerns, you should duplicate this backend.tf file in those directories with a different prefix so your state bucket matches your directory layout.

5. Now terraform can transfer state from your local environment into GCP. From the cicd directory:
    ```shell
    terraform init -force-copy
    ```

6. Follow the instructions at https://source.cloud.google.com/<project name>/<repository name> to then push your code (from the parent directory of cicd, i.e. not the cicd directory) into your new CICD pipeline. Basically:

    ```shell
    git init
    gcloud init && git config --global credential.https://source.developers.google.com.helper gcloud.sh
    git remote add google  https://source.developers.google.com/p/<project name>/r/<repository name>
    git checkout -b main
    git add cicd/configs/* cicd/backend.tf cicd/main.tf cicd/outputs.tf cicd/terraform.tfvars cicd/triggers.tf cicd/variables.tf
    git commit -m 'first push after bootstrap'
    git push --all google

7. After the repo and pipeline is established you should be able to view the build triggers and history by visiting:
https://console.cloud.google.com/cloud-build/dashboard?project=<project id here>


## Cloud run container ##
The /cloudrun directory is where you will work with terraform to publish the container you intend to serve using Cloudrun.

tl;dr 
main.tf is the terraform to tweak, and /cloudrun/container is the Dockerfile, cloudbuild.yaml and place to put your container source.

Be sure to set terraform.tvfars to reference your target project ID.

See /cloudrun/README.md for details.


## CICD Container/Container Creation

The Docker container used for CICD executions are inspired by those built and maintained by the
Cloud Foundation Toolkit (CFT) team.


Documentations and source can be found [here](https://github.com/GoogleCloudPlatform/cloud-foundation-toolkit/tree/master/infra/build/developer-tools-light). Images can be found [here](https://console.cloud.google.com/gcr/images/cloud-foundation-cicd/GLOBAL/cft/developer-tools-light).

This version of the container includes necessary dependencies (e.g. bash, terraform, gcloud, python, pip, pipenv) to validate and deploy Terraform configs and is based on hashicorp's native terraform and alpine linux.

To build the container, cd to the container directory and issue the command

```bash
gcloud builds submit
```
Which will kick off a build using the cloudbuild.yaml and Dockerfile in the container directory, creating a 'cloudbuilder' container ( gcr.io/${PROJECT_ID}/cloudbuilder )in your project that is used by the triggers.




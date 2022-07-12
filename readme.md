#Assignment 2 & 3

The HttpExample folder contains the code for a basic python function app that gets the secret of a keyvault and returns an http response in the style that was requested by the assignment.

The azure-pipelines.yml is the file that azure devops uses for it's pipeline to deploy the function app.
Below is an image of the pipeline working

![Pipeline](/images/pipeline.png)

You may also test it using https://dfx-testkv1.azurewebsites.net/api/HttpExample?name=VaronisAssignmentSecret

# cloud-translate-project-fresh

If you wish to deploy the Application on your own, follow these steps:
- Building the docker image: `docker build -t document-translator:latest .`  
- Testing locally: `docker run -p 5000:5000 document-translator:latest`  

After all the testing were done, the deployment begins:
- To deploy, the commands `az login` and `az acr login` had to be used to correctly identify which acr to correctly deploy.  
- Then the docker image was tagged latest using the following command `docker tag document-translator:latest tradappthp.azurecr.io/document-translator:latest`   
- Finally, the tagged image was pushed to the ACR by the command `docker push tradappthp.azurecr.io/document-translator:latest`  

Before the webapp can be used, there are certain steps to be done.
- First, an identity for the WebApp is needed. It can simply be done by enabling `System Identity`.
- Next is assigning roles to the WebApp. By default, the WebApp doesn't have any role assignments therefore, it cannot access anything.  
    The WebApp needs access to the ACR to pull the latest docker image that was pushed and deploy it to himself.  
    Hence, granting the permission of `AcrPull` is crucial.
- Lastly, making the WebApp deploy the image from the ACR so that the webapp will automatically deploy the lastest image pushed to the ACR.  
    It can be done by adjusting the Deployment Center Settings of the WebApp. 

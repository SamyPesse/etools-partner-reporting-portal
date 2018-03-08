# etools-partner-reporting-portal

## Container build status

* Polymer: 

  ![Codefresh build status](https://g.codefresh.io/api/badges/build?repoOwner=unicef&repoName=etools-partner-reporting-portal&branch=develop&pipelineName=polymer&accountName=unicef&type=cf-1)

* PostGIS: 

  ![Codefresh build status](https://g.codefresh.io/api/badges/build?repoOwner=unicef&repoName=etools-partner-reporting-portal&branch=develop&pipelineName=db&accountName=unicef&type=cf-1)

* Django API: 

  ![Codefresh build status](https://g.codefresh.io/api/badges/build?repoOwner=unicef&repoName=etools-partner-reporting-portal&branch=develop&pipelineName=django_api&accountName=unicef&type=cf-1)

* Nginx proxy: 

  ![Codefresh build status](https://g.codefresh.io/api/badges/build?repoOwner=unicef&repoName=etools-partner-reporting-portal&branch=develop&pipelineName=proxy&accountName=unicef&type=cf-1)

## Setup

1. Install Docker for your OS. Also install Fabric via `pip install fabric`.
2. Create .env file in `django_api` with the reference of `.env.example` or receive .env file from your team member.
3. Run `fab up` !
4. Go to [http://127.0.0.1:8080/](http://127.0.0.1:8080/) to see the frontend / polymer running. The Django app is running under [http://127.0.0.1:8080/api/](http://127.0.0.1:8080/api/)
5. Run `fab fixtures` - load fake data like account, core, partner and other modules!
6. TEMP: Go to [http://127.0.0.1:8080/api/admin/](http://127.0.0.1:8080/api/admin/) login with admin/Passw0rd! and can now go to [http://127.0.0.1:8080/app/](http://127.0.0.1:8080/app/) to see the frontend interface. Replace 'ip-reporting' or 'cluster-reporting' in the URL's to switch between the two interfaces.

## Development

Here are some docker tips:  
   1. display all containers:

```text
   $ docker-compose ps
```

1. ssh into running django\_api container

   ```text
   $ fab ssh:django_api
   ```

2. Stop all containers

   ```text
   $ fab stop
   ```

3. Re-build docker images for containers

   ```text
   $ fab rebuild
   ```


# Creating Requirements

Command to generate requirements.txt: `pipdeptree -f | tee requirements.txt`

# Deploying

The database was deployed in AWS RDS free tier instance.

The website was deployed in Heroku. Check heroku docs to configure the environment to deploy.

Execute the following command:

`git push heroku `git subtree split --prefix ceca main`:master --force`.
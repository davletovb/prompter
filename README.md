# Prompter

Prompter is a simple web app that allows users to prompt OpenAI API, by registering and paying for monthly subscription. 
It also has an admin panel, where admins can see users, their payment status and number of prompts they used.

## Usage

* Install required libraries:
```
pip install -r requirements.txt
```

* Set environment variables: 
```
export SECRET_KEY="SECRET_KEY"
export DATABASE_URL="DATABASE_URL"
export STRIPE_SECRET_KEY="STRIPE_SECRET_KEY"
export STRIPE_PUBLISHABLE_KEY="STRIPE_PUBLISHABLE_KEY"
export OPENAI_API_KEY="OPENAI_API_KEY"
```

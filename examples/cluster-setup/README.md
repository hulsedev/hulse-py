# Cluster Setup

Read these instructions to get an idea of how to setup your first Hulse cluster using the `hulse-py` CLI.

## Getting Started

Make sure you've already gone through the installation steps detailed in the root `README.md` file. We assume you already have your environment setup with the latest version of `hulse-py` available.

First, login to your Hulse account from your terminal:
```bash
hulse login
```
> This should redirect you to your default web browser. Login and come back to your terminal. Alternatively, you may choose to log in manually by running `hulse init`. This command will prompt you for your email, username, and API key linked to your Hulse account.

Next, create your first cluster:
```bash
hulse create-cluster --name="your-cluster-name" --description="your-cluster-description"
```

And that's it! You've created your first Hulse cluster! 

You can now list your clusters:
```bash
hulse get-clusters
```

And share their cluster ids with your team to leverage your computing power.
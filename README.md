## Dependencies

`globus_sdk` and `requests`, although installing `globus_sdk` will automatically
ensure that requests is up-to-date.

Use `download_install_miniconda3.sh` and `setup_dnasc_env.sh` to get python
ready and the packages installed. Use `$ conda activate dnascapp_env` to enter the virtual environment.

## Access to app credentials

For security, the Globus and SMRT Link credentials created for use by 
the app are stored exclusively in a file in `/home/dnascapp/backend`.

In order for the credentials to be accessible when a user other than
dnascapp runs the program, the proper ACLs must be set.

```
chown :fslg_dnasc /home/dnascapp
chown :fslg_dnasc /home/dnascapp/backend
chmod 710 /home/dnascapp
chmod 710 /home/dnascapp/backend
chmod 740 /home/dnascapp/backend/credentials.json
```
conda=/home/dnascapp/miniconda3/bin/conda
$conda create --name dnascapp_env
# important: conda activate is not available non-interactively
# therefore, use source to activate the environment
source /home/dnascapp/miniconda3/bin/activate dnascapp_env
$conda install python
$conda install sqlite
$conda install openssl
$conda install urllib3
python -m pip install globus_sdk
python -m pip install globus_sdk --upgrade
# add pythonpath variable to dnascapp_env
$conda env config vars set PYTHONPATH=/home/aknaupp/backend --name dnascapp_env
if [[ -z $PYTHONPATH ]]
then
    echo "Failed to set PYTHONPATH, please set it manually"
fi
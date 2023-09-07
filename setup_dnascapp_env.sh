conda="/home/dnascapp/miniconda3/condabin/conda"
$conda create --name dnascapp_env
$conda activate dnascapp_env
$conda install python
$conda install sqlite
$conda install openssl
$conda install urllib3
python -m pip install globus_sdk
$conda deactivate
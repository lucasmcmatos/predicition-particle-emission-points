@echo off
echo ==========================================
echo SETTING UP TENSORFLOW ENVIROMENT WITH GPU
echo ==========================================

:: Creating Conda enviroment with Python 3.10
echo [1/6] Creating Conda enviroment...
conda create -y -n tf-gpu python=3.10

:: Activating enviroment
echo [2/6] Activating enviroment...
call conda activate tf-gpu

:: Downloading CUDA Toolkit and cuDNN compatible by conda-forge
echo [3/6] Downloaing CUDA Toolkit 11.8 and cuDNN 8.6.0...
conda install -y -c conda-forge cudatoolkit=11.8 cudnn=8.6.0

:: Downloads TensorFlow 2.13 with GPU suport
echo [4/6] Downloading TensorFlow 2.13...
pip install tensorflow==2.13

:: Downloads Jupyter and kernel for the enviroment
echo [5/6] Download Jupyter and creating kernel...
pip install notebook ipykernel
python -m ipykernel install --user --name=tf-gpu --display-name "Python (tf-gpu)"

echo [6/6] Complete! Execute 'jupyter notebook' at tf-gpu enviroment.
pause

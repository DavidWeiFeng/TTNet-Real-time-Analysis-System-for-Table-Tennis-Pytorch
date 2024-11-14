@echo off

:: 如果需要激活虚拟环境，取消下面这行的注释并修改路径
:: call path\to\your\venv\Scripts\activate.bat
call D:\UGit\TTNet-Real-time-Analysis-System-for-Table-Tennis-Pytorch\.venv\Scripts\activate.bat


python main.py ^
--working-dir "../" ^
--saved_fn "ttnet_1st_phase" ^
--no-val ^
--batch_size 8 ^
--num_workers 4 ^
--lr 0.001 ^
--lr_type "step_lr" ^
--lr_step_size 10 ^
--lr_factor 0.1 ^
--gpu_idx 0 ^
--global_weight 5. ^
--seg_weight 1. ^
--no_local ^
--no_event ^
--smooth-labelling

:: 如果你想在运行完后暂停窗口
pause 
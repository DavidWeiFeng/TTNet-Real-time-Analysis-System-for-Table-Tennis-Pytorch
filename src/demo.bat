@echo off

:: 激活虚拟环境（取消注释并修改为你的虚拟环境路径）
call D:\UGit\TTNet-Real-time-Analysis-System-for-Table-Tennis-Pytorch\.venv\Scripts\activate.bat

python demo.py ^
--working-dir "../" ^
--saved_fn "demo" ^
--arch "ttnet" ^
--gpu_idx 0 ^
--pretrained_path "D:\UGit\TTNet-Real-time-Analysis-System-for-Table-Tennis-Pytorch\project_root\checkpoints\ttnet\ttnet_epoch_2.pth" ^
--seg_thresh 0.5 ^
--event_thresh 0.5 ^
--thresh_ball_pos_mask 0.05 ^
--video_path "../dataset/test/videos/test_6.mp4" ^
--show_image ^
--save_demo_output

:: 如果你想在运行完后暂停窗口
pause 
import os
from glob import glob
import json

import cv2


def make_folder(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)


def get_frame_indexes(events_annos_path, num_frames_from_event):
    """
    从事件标注文件中获取需要提取的帧索引
    
    Args:
        events_annos_path: 事件标注JSON文件的路径
        num_frames_from_event: 事件帧前后需要提取的帧数
        
    Returns:
        set: 需要提取的帧索引集合
    """
    json_file = open(events_annos_path)
    events_annos = json.load(json_file)
    selected_indexes = []
    main_frames = sorted(events_annos.keys())
    for main_f_idx in main_frames:
        event = events_annos[main_f_idx]
        main_f_idx = int(main_f_idx)
        # 对于每个事件帧，提取其前后的帧
        if event == 'empty_event':  # 对于空事件，提取前后各4帧
            for idx in range(main_f_idx - num_frames_from_event, main_f_idx + num_frames_from_event + 1):
                selected_indexes.append(idx)
        else:  # 对于非空事件，提取前后各8帧
            for idx in range(main_f_idx - num_frames_from_event * 2, main_f_idx + num_frames_from_event * 2 + 1):
                selected_indexes.append(idx)
    selected_indexes = set(selected_indexes)  # 去除重复的帧索引
    return selected_indexes


def extract_images_from_videos(video_path, events_annos_path, out_images_dir, num_frames_from_event):
    """
    从视频中提取指定帧并保存为图片
    
    Args:
        video_path: 视频文件路径
        events_annos_path: 事件标注文件路径
        out_images_dir: 输出图片目录
        num_frames_from_event: 事件帧前后需要提取的帧数
    """
    # 获取需要提取的帧索引
    selected_indexes = get_frame_indexes(events_annos_path, num_frames_from_event)

    # 设置输出目录
    video_fn = os.path.basename(video_path)[:-4]
    sub_images_dir = os.path.join(out_images_dir, video_fn)
    make_folder(sub_images_dir)

    # 打开视频文件
    video_cap = cv2.VideoCapture(video_path)
    n_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    f_width = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    f_height = video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video_cap.get(cv2.CAP_PROP_FPS)
    
    # 打印视频信息
    print('*-' * 20)
    print('Processing video {}.mp4'.format(video_fn))
    print('Frame rate: {}, f_width: {}, f_height: {}'.format(fps, f_width, f_height))
    print('number of frames in the video: {}, number of selected frames: {}'.format(n_frames, len(selected_indexes)))
    
    # 逐帧处理视频
    frame_cnt = -1
    processed_frames = 0
    total_selected = len(selected_indexes)
    
    while True:
        ret, img = video_cap.read()
        if ret:
            frame_cnt += 1
            if frame_cnt in selected_indexes:
                processed_frames += 1
                
                image_path = os.path.join(sub_images_dir, 'img_{:06d}.jpg'.format(frame_cnt))
                if os.path.isfile(image_path):
                    continue
                cv2.imwrite(image_path, img)
            # 显示处理进度：当前帧/总帧数，已处理帧数/需要处理的总帧数
            print('\r当前帧: [{}/{}] | 已处理: [{}/{}] 帧'.format(
                frame_cnt, int(n_frames),
                processed_frames, total_selected
            ), end='')
        else:
            break
    
    video_cap.release()
    print('\n完成提取: {}'.format(video_path))


if __name__ == '__main__':
    # 设置数据集目录和参数
    dataset_dir = './dataset'
    num_frames_sequence = 9  # 论文提到使用25帧，但实际使用9帧
    num_frames_from_event = int((num_frames_sequence - 1) / 2)  # 计算事件帧前后需要提取的帧数
    
    # 处理训练集和测试集
    for dataset_type in ['training', 'test']:
        # 设置输入输出路径
        video_dir = os.path.join(dataset_dir, dataset_type, 'videos')
        annos_dir = os.path.join(dataset_dir, dataset_type, 'annotations')
        out_images_dir = os.path.join(dataset_dir, dataset_type, 'images')

        # 获取所有视频文件
        video_paths = glob(os.path.join(video_dir, '*.mp4'))
        total_videos = len(video_paths)

        # 处理每个视频文件
        for video_idx, video_path in enumerate(video_paths):
            print('\n处理视频 [{}/{}]'.format(video_idx + 1, total_videos))
            video_fn = os.path.basename(video_path)[:-4]
            events_annos_path = os.path.join(annos_dir, video_fn, 'events_markup.json')
            extract_images_from_videos(video_path, events_annos_path, out_images_dir, num_frames_from_event)

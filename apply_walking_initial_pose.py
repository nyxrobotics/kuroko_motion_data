import os

import yaml


def load_joint_positions(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        return {k: v.get('position', 0.0) for k, v in data.get('joints', {}).items()}


def apply_difference_to_frame(path, diff):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    if "joints" not in data:
        return  # skip if no joints

    for joint, joint_data in data["joints"].items():
        if "position" in joint_data and joint in diff:
            joint_data["position"] += diff[joint]

    with open(path, 'w') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print(f"✅ Updated: {path}")


def process_animation_directory(anim_dir, diff):
    target_files = ["animation.yaml", "initial_frame.yaml"]
    for fname in target_files:
        path = os.path.join(anim_dir, fname)
        if os.path.isfile(path):
            apply_difference_to_frame(path, diff)

    frames_dir = os.path.join(anim_dir, "frames")
    if os.path.isdir(frames_dir):
        for frame_file in os.listdir(frames_dir):
            if frame_file.endswith(".yaml"):
                apply_difference_to_frame(
                    os.path.join(frames_dir, frame_file), diff)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Use walking_initial_pose.yaml for both old and new pose
    initial_pose_path = os.path.join(script_dir, "initial_pose.yaml")
    walking_pose_path = os.path.join(script_dir, "walking_initial_pose.yaml")
    pose_old = load_joint_positions(initial_pose_path)
    pose_new = load_joint_positions(walking_pose_path)

    # Compute difference (this will result in all zero unless changed for specific case)
    diff = {}
    for joint in pose_new:
        if joint in pose_old:
            diff[joint] = pose_new[joint] - pose_old[joint]

    # Walk through all subdirectories in the current directory (workspace)
    for subdir in os.listdir("."):
        if os.path.isdir(subdir):
            process_animation_directory(subdir, diff)

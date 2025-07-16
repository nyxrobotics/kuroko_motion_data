
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

if __name__ == "__main__":
    # Load initial poses from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pose_old = load_joint_positions(os.path.join(script_dir, "initial_pose_old.yaml"))
    pose_new = load_joint_positions(os.path.join(script_dir, "initial_pose.yaml"))

    # Compute position differences
    diff = {}
    for joint in pose_new:
        if joint in pose_old:
            diff[joint] = pose_new[joint] - pose_old[joint]

    # Apply to all YAML frames in the execution directory (not script_dir)
    for filename in os.listdir("."):
        if filename.endswith(".yaml") and not filename.startswith("initial_pose"):
            apply_difference_to_frame(filename, diff)
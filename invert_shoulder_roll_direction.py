import os
import yaml

TARGET_JOINTS = ["shoulder_r_roll", "shoulder_l_roll"]

def invert_shoulder_roll_signs(path):
    with open(path, 'r') as f:
        content = yaml.safe_load(f)

    joints = content.get("joints", {})
    modified = False

    for joint_name in TARGET_JOINTS:
        if joint_name in joints and 'position' in joints[joint_name]:
            position = joints[joint_name]['position']
            if isinstance(position, (int, float)):
                joints[joint_name]['position'] = -position
                modified = True

    if modified:
        with open(path, 'w') as f:
            yaml.dump(content, f, allow_unicode=True, sort_keys=False)
        print(f"✅ Updated: {path}")
    else:
        print(f"ℹ️ No update needed: {path}")

# Example: update all YAML files in the current directory
if __name__ == "__main__":
    for filename in os.listdir("."):
        if filename.endswith(".yaml"):
            invert_shoulder_roll_signs(filename)

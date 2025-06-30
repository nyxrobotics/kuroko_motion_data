import os
import yaml
import copy

# 左右スワップ対象のプレフィックスペア
SWAP_KEYS = [
    ("ankle_l_", "ankle_r_"),
    ("elbow_l_", "elbow_r_"),
    ("hip_l_", "hip_r_"),
    ("shin_l_", "shin_r_"),
    ("shoulder_l_", "shoulder_r_"),
    ("thigh_l_", "thigh_r_"),
]

# position符号を変えない例外関節キー（完全名）
EXCLUDE_INVERT = {"hip_r_roll", "hip_l_roll"}

# 左右スワップはしないがpositionだけ反転するキー
INVERT_ONLY = {"chest"}

def invert_position(joint_name, joint_data):
    """position の符号を反転（例外を除く）"""
    if 'position' in joint_data and isinstance(joint_data['position'], (int, float)):
        if joint_name not in EXCLUDE_INVERT:
            joint_data['position'] = -joint_data['position']
    return joint_data

def process_file(path):
    with open(path, 'r') as f:
        content = yaml.safe_load(f)

    joints = content.get("joints", {})
    speed = content.get("speed_scale", {})

    # 左右スワップ + position反転
    for l_prefix, r_prefix in SWAP_KEYS:
        l_keys = [k for k in joints if k.startswith(l_prefix)]
        for l_key in l_keys:
            r_key = l_key.replace(l_prefix, r_prefix)
            if r_key in joints:
                left = copy.deepcopy(joints[l_key])
                right = copy.deepcopy(joints[r_key])
                joints[l_key] = invert_position(r_key, right)
                joints[r_key] = invert_position(l_key, left)

    # chest だけposition符号反転（スワップしない）
    if "chest" in joints:
        joints["chest"] = invert_position("chest", joints["chest"])

    # speed_scale スワップ（値そのものは反転しない）
    for l_prefix, r_prefix in SWAP_KEYS:
        l_keys = [k for k in speed if k.startswith(l_prefix)]
        for l_key in l_keys:
            r_key = l_key.replace(l_prefix, r_prefix)
            if r_key in speed:
                speed[l_key], speed[r_key] = speed[r_key], speed[l_key]

    # 書き戻し
    with open(path, 'w') as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False)

    print(f"✅ Updated: {path}")

# 実行
if __name__ == "__main__":
    for filename in os.listdir("."):
        if filename.endswith(".yaml"):
            process_file(filename)

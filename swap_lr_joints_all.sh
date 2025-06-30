#!/bin/bash

for file in *.yaml; do
  echo "🌀 Processing $file"
  TMP_FILE=$(mktemp)

  # 左右の関節名を一時置換
  sed -E '
    s/elbow_l_/__TEMP_ELBOW_R_/g;
    s/elbow_r_/__TEMP_ELBOW_L_/g;
    s/ankle_l_/__TEMP_ANKLE_R_/g;
    s/ankle_r_/__TEMP_ANKLE_L_/g;
    s/hip_l_/__TEMP_HIP_R_/g;
    s/hip_r_/__TEMP_HIP_L_/g;
    s/shin_l_/__TEMP_SHIN_R_/g;
    s/shin_r_/__TEMP_SHIN_L_/g;
    s/shoulder_l_/__TEMP_SHOULDER_R_/g;
    s/shoulder_r_/__TEMP_SHOULDER_L_/g;
    s/thigh_l_/__TEMP_THIGH_R_/g;
    s/thigh_r_/__TEMP_THIGH_L_/g
  ' "$file" > "$TMP_FILE"

  # 一時置換を本来の反対に戻す
  sed -E '
    s/__TEMP_ELBOW_R_/elbow_r_/g;
    s/__TEMP_ELBOW_L_/elbow_l_/g;
    s/__TEMP_ANKLE_R_/ankle_r_/g;
    s/__TEMP_ANKLE_L_/ankle_l_/g;
    s/__TEMP_HIP_R_/hip_r_/g;
    s/__TEMP_HIP_L_/hip_l_/g;
    s/__TEMP_SHIN_R_/shin_r_/g;
    s/__TEMP_SHIN_L_/shin_l_/g;
    s/__TEMP_SHOULDER_R_/shoulder_r_/g;
    s/__TEMP_SHOULDER_L_/shoulder_l_/g;
    s/__TEMP_THIGH_R_/thigh_r_/g;
    s/__TEMP_THIGH_L_/thigh_l_/g
  ' "$TMP_FILE" > "$file"

  rm "$TMP_FILE"
  echo "✅ Finished $file"
done

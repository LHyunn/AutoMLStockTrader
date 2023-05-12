import streamlit as st
import os
import pandas as pd
from glob import glob
import time
import subprocess
from natsort import natsorted

def tail(file_path):
    cmd = ['tail', '-f', file_path]
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = popen.stdout.readline()
        if not line:
            break
        yield line.strip().decode('utf-8')
#log_list 
log_list = glob("/app/output/**/*.log", recursive=True)

log_selectbox = st.selectbox("로그", log_list, index=0, key="log_selectbox")
log_path = f"{log_selectbox}"
log_dir = "/".join(log_path.split("/")[:-1])

log_lines = st.empty()
img_lines = st.empty()
count = 0
for line in tail(log_path):
    log_lines.text(line)
    if "Elapsed" in line:
        st.success("학습 완료.")
        img_list = glob(f"{log_dir}/**/*.png", recursive=True)
        img_list = natsorted(img_list)
        if len(img_list) > 0:
            img_lines.image(img_list, width=800)
        break
    count = count + 1
    if count > 10:
        count = 0
        try:
            img_list = glob(f"{log_dir}/**/*.png", recursive=True)
            img_list = natsorted(img_list)
            if len(img_list) > 0:
                img_lines.image(img_list, width=800)
        except:
            pass
    time.sleep(0.1)
    



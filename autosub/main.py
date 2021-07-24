#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import wave
import argparse
import subprocess
import numpy as np
from tqdm import tqdm
# from deepspeech import Model, version 
from segmentAudio import silenceRemoval
from audioProcessing import extract_audio, convert_samplerate
from writeToFile import write_to_file
import os
import speech_recognition as sr



# Line count for SRT file
line_count = 0

def sort_alphanumeric(data):
    """Sort function to sort os.listdir() alphanumerically
    Helps to process audio files sequentially after splitting 

    Args:
        data : file name
    """
    
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    
    return sorted(data, key = alphanum_key)


def ds_process_audio( audio_file, file_handle):  
    # Perform inference on audio segment
    global line_count
    try:
        r=sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data=r.record(source)
            text=r.recognize_google(audio_data)
            print(text)
            infered_text = text
    except:
        infered_text=""
        pass

    # infered_text = ds.stt(audio)
    
    # File name contains start and end times in seconds. Extract that
    limits = audio_file.split("/")[-1][:-4].split("_")[-1].split("-")
    
    if len(infered_text) != 0:
        line_count += 1
        write_to_file(file_handle, infered_text, line_count, limits)


def main():
    global line_count
    print("AutoSub v0.1\n")
        
    parser = argparse.ArgumentParser(description="AutoSub v0.1")
    parser.add_argument('--model', required=False,
                        help='DeepSpeech model file')
    parser.add_argument('--scorer',
                        help='DeepSpeech scorer file')
    parser.add_argument('--file', required=False,
                        help='Input video file')
    args = parser.parse_args()
    
    # ds_model = args.model
    # if not ds_model.endswith(".pbmm"):
    #     print("Invalid model file. Exiting\n")
    #     pass
    
    # # Load DeepSpeech model 
    # ds = Model(ds_model)
            
    # if args.scorer:
    #     ds_scorer = args.scorer
    #     if not ds_scorer.endswith(".scorer"):
    #         print("Invalid scorer file. Running inference using only model file\n")
    #     else:
    #         ds.enableExternalScorer(ds_scorer)
    
    input_file = args.file
    print("\nInput file:", input_file)
    
    base_directory = os.getcwd()
    output_directory = os.path.join(base_directory, "output")
    audio_directory = os.path.join(base_directory, "audio")
    video_file_name = input_file.split("/")[-1].split(".")[0]
    audio_file_name = os.path.join(audio_directory, video_file_name + ".wav")
    srt_file_name = os.path.join(output_directory, video_file_name + ".srt")
    
    # Extract audio from input video file
    extract_audio(input_file, audio_file_name)
    
    print("Splitting on silent parts in audio file")
    silenceRemoval(audio_file_name)
    
    # Output SRT file
    file_handle = open(srt_file_name, "w")
    
    print("\nRunning inference:")
    
    for file in tqdm(sort_alphanumeric(os.listdir(audio_directory))):
        audio_segment_path = os.path.join(audio_directory, file)
        
        # Dont run inference on the original audio file
        if audio_segment_path.split("/")[-1] != audio_file_name.split("/")[-1]:
            ds_process_audio(audio_segment_path, file_handle)
            
    print("\nSRT file saved to", srt_file_name)
    file_handle.close()
        
if __name__ == "__main__":
    main()
# Demo Audio

把測試用的微試教錄音檔放在這個資料夾。

**建議命名**：`<日期>_<主題>_<時長>.mp3`
範例：`20260428_water_three_states_3min.mp3`

**已 gitignore**：`.mp3 / .wav / .m4a` 不會被 commit，避免敏感資料外流。

## 自製測試音檔

最快方法（macOS）：
```bash
say -o demo.aiff "今天我們要上水的三態。固態的水叫什麼？冰。對就是冰。"
ffmpeg -i demo.aiff demo.mp3
```

## W1 P0 任務：跑你 4-25 觀課錄音

memory 提到 2026-04-25 三堂連續觀課。把任一堂的錄音放這，跑：
```bash
python -c "from lib.openai_whisper import transcribe; \
  print(transcribe('tests/demo_audio/<檔名>.mp3'))"
```
看 Whisper 對你錄音檔的 WER baseline，這是 W1 必須產出的數據。

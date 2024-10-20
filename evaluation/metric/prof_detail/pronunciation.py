# 한글 wav2vec+커스텀 데이터셋
# 필요한 라이브러리 임포트
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from torch import nn
from torch.optim import Adam
from torch.utils.data import DataLoader
import numpy as np
from tqdm import tqdm
import os
from pydub import AudioSegment

# Hugging Face에서 사전 학습된 Wav2Vec2 모델 로드
# processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
# base_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-960h")
processor = Wav2Vec2Processor.from_pretrained("kresnik/wav2vec2-large-xlsr-korean")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

base_model = Wav2Vec2ForCTC.from_pretrained("kresnik/wav2vec2-large-xlsr-korean").to(device)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 발음 평가를 위한 모델 정의
class PronunciationAssessmentModel(nn.Module):
    def __init__(self, base_model):
        super(PronunciationAssessmentModel, self).__init__()
        self.base_model = base_model  # 사전 학습된 모델 사용
        # LSTM 레이어 추가 (입력 크기 1024, 양방향)
        self.blstm = nn.LSTM(input_size=1024, hidden_size=128, num_layers=1, bidirectional=True, batch_first=True)
        # 최종 출력 레이어 (출력 크기 1)
        self.fc = nn.Linear(256, 1)  # 128 * 2 for bidirectional LSTM

    def forward(self, input_values):
        # 사전 학습된 모델을 사용하여 특성 추출
        with torch.no_grad():
            outputs = self.base_model(input_values, output_hidden_states=True)
            hidden_states = torch.stack(outputs.hidden_states, dim=0)  # (num_layers, batch_size, seq_len, hidden_size)
            # 마지막 레이어의 hidden state 사용
            context_representation = hidden_states[-1]  # (batch_size, seq_len, hidden_size)
        # LSTM 레이어를 통해 출력 계산
        lstm_output, _ = self.blstm(context_representation)
        # 글로벌 평균 풀링 적용
        output = torch.mean(lstm_output, dim=1)
        # 최종 출력 계산
        output = self.fc(output)
        return output

# 저장된 모델 불러오기 및 평가
def load_model(model_save_path, base_model, device):
    # 모델을 불러올 때 동일한 모델 구조를 생성해야 함
    loaded_model = PronunciationAssessmentModel(base_model).to(device)

    # 저장된 상태 사전 불러오기
    loaded_model.load_state_dict(torch.load(model_save_path, map_location=device))

    # 모델을 평가 모드로 설정 (필수, 모델을 사용할 때는 평가 모드로 설정해야 함)
    loaded_model.eval()

    print("Model loaded and ready for evaluation")
    return loaded_model

# 오디오 파일 인퍼런스 함수
def infer_pronunciation(model, audio_tensor, processor):
    model.eval()  # 모델을 평가 모드로 설정

    # 입력 데이터를 텐서로 변환하고 배치를 추가 (모델 입력 형식 맞춤)
    input_values = audio_tensor.unsqueeze(0).to(device)  # 모델과 동일한 장치로 이동

    with torch.no_grad():
        # 모델 예측값 계산
        prediction = model(input_values)

    # 예측된 발음 점수 반환
    return prediction.item()

# 새로운 함수 정의
def get_pronunciation_score(input_audio_list):
    scores = []
    for audio_data in input_audio_list:
        # mp3 AudioSegment 객체를 wav로 변환
        audio = audio_data['audio'].set_frame_rate(16000).set_channels(1)
        audio_path = f"/tmp/{audio_data['title']}.wav"
        audio.export(audio_path, format="wav")

        # 오디오 파일 로드
        # waveform, sample_rate = torchaudio.load(audio_path)
        waveform, sample_rate = torchaudio.load(audio_path, format="wav")

        if sample_rate != 16000:
            waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)
        waveform = waveform.squeeze(0)  # 채널 차원 제거

        # 발음 점수 예측
        score = infer_pronunciation(loaded_model, waveform, processor)
        scores.append({
            'title': audio_data['title'],
            'score': score
        })
    return scores

# 저장된 모델 경로 설정
model_save_path = "model/assessment_model.pth"  # 저장된 모델 파일 경로

# 모델 불러오기
loaded_model = load_model(model_save_path, base_model, device)

# 예제 오디오 리스트 평가
input_audio_list = [
    {
        'title': 'USER_0001',
        'audio': AudioSegment.from_mp3("data/test_audio/USER_0001.mp3")
    },
    {
        'title': 'USER_0002',
        'audio': AudioSegment.from_mp3("data/test_audio/USER_0002.mp3")
    }
]

# 발음 점수 가져오기
scores = get_pronunciation_score(input_audio_list)
for score in scores:
    print(f"Title: {score['title']}, Predicted Pronunciation Score: {score['score']:.2f}")

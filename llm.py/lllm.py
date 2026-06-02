# -----------------------------------------------------------------------------------------------
# 이건 소설을 불러올것인데 이것 read할것이고 UTF-8 방식으로 해석해라는것 같아
# -----------------------------------------------------------------------------------------------
import urllib.request

url = (
    "https://raw.githubusercontent.com/rickiepark/"
    "llm-from-scratch/main/ch02/01_main-chapter-code/"
    "the-verdict.txt"
)

file_path = "the-verdict.txt"
urllib.request.urlretrieve(url, file_path)

with open(file_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

print("총 문자 개수:", len(raw_text))
print(raw_text[:99])


# -----------------------------------------------------------------------------------------------
# 이것을 통해서 우리는 입력값의 문장이나 입력값들을 토큰으로 바꿀수있게 된다
# -----------------------------------------------------------------------------------------------
import re

text = "Hello, world. This, is a test."
result = re.split(r"([,.]|\s)", text)
# 나늘때 단위를 띄워쓰기 ,. 단어 기준으로 나눈다.
result = [item for item in result if item.strip()]
# 아무내용이 없는 공백은 삭제
print(result)


# -----------------------------------------------------------------------------------------------
import urllib.request
import re

url = (
    "https://raw.githubusercontent.com/rickiepark/"
    "llm-from-scratch/main/ch02/01_main-chapter-code/"
    "the-verdict.txt"
)

file_path = "the-verdict.txt"
urllib.request.urlretrieve(url, file_path)

with open(file_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
# item.strip() 이차이는 앞뒤 공백삭제이다.
print(len(preprocessed))
print(preprocessed[:30])


# -----------------------------------------------------------------------------------------------
# 토큰을 토큰id로 변화시킨다
# -----------------------------------------------------------------------------------------------

# 먼저 어휘사전을 꺼낸다 즉 이미 이 소설에 대한 모든 토큰들에 대한 학습과 토큰id가 모두 들어가있는 table 과 같다고 생각하면돤다
all_words = sorted(set(preprocessed))
vocab_size = len(all_words)
print("vocab_size is", vocab_size)
vocab = {token: integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break


# -----------------------------------------------------------------------------------------------
# 텍스트를 숫자로 바꾸고, 그 숫자를 다시 텍스트로 되돌리는 기계 만들기.
# -----------------------------------------------------------------------------------------------

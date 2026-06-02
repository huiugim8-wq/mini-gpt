# -*- coding: utf-8 -*-
"""
UTF-8 byte-level BPE 토크나이저 과제 템플릿.

외부 tokenizer 라이브러리 없이 BPE(Byte Pair Encoding)를 직접 구현합니다.
한국어 NSMC 리뷰를 다루므로 문자열을 글자/공백 단위로 먼저 자르지 말고,
항상 `text.encode("utf-8")`로 byte ID 시퀀스를 만든 뒤 merge를 적용하세요.
"""

from collections import Counter
from pathlib import Path

PAD_TOKEN = "<pad>"
# 실제 내용은 아니고 자리만 채우는 토큰
UNK_TOKEN = "<unk>"
# 모르는 토큰
BOS_TOKEN = "<bos>"
EOS_TOKEN = "<eos>"
# <bos> 나는 학교에 갔다. <eos>

SPECIAL_TOKENS = [PAD_TOKEN, UNK_TOKEN, BOS_TOKEN, EOS_TOKEN]
SPECIAL_IDS = {token: idx for idx, token in enumerate(SPECIAL_TOKENS)}
BYTE_OFFSET = len(SPECIAL_TOKENS)
NUM_BYTES = 256


class BPETokenizer:
    """
    UTF-8 byte-level BPE 토크나이저.

    권장 ID 배치:
    - 0~3: <pad>, <unk>, <bos>, <eos>
    - 4~259: 원본 byte 0~255
    - 260 이상: BPE merge로 생성한 토큰
    """

    def __init__(self, vocab_size: int = 3000):
        self.vocab_size = vocab_size
        self.id_to_token = {}
        self.token_to_id = {}
        self.merges = []

    def _init_special_tokens(self):
        # TODO:
        # 1. 특수 토큰 4개를 고정 ID 0~3에 등록합니다.

        # 1. 특수 토큰 4개를 고정 ID 0~3에 등록합니다.
        for idx, token in enumerate(SPECIAL_TOKENS):
            self.id_to_token[idx] = token
            self.token_to_id[token] = idx

        # 2. byte 0~255를 ID 4~259에 bytes([byte_value]) 형태로 등록합니다.
        for byte_value in range(NUM_BYTES):
            token_id = BYTE_OFFSET + byte_value
            token = bytes([byte_value])
            self.id_to_token[token_id] = token
            self.token_to_id[token] = token_id

        # 우리가 utf-8기준으로 활용한다묜 255 개의 기본 값을 정의할수잇다

    def get_pad_id(self):
        """padding 토큰 ID."""
        return SPECIAL_IDS[PAD_TOKEN]

    def get_unk_id(self):
        """unknown 토큰 ID."""
        return SPECIAL_IDS[UNK_TOKEN]

    def get_bos_id(self):
        """문장 시작 토큰 ID."""
        return SPECIAL_IDS[BOS_TOKEN]

    def get_eos_id(self):
        """문장 끝 토큰 ID."""
        return SPECIAL_IDS[EOS_TOKEN]

    def train(self, corpus: str):
        self.id_to_token = {}
        self.token_to_id = {}
        self.merges = []
        self._init_special_tokens()
        ids = [BYTE_OFFSET + byte_value for byte_value in corpus.encode("utf-8")]

        while len(self.id_to_token) < self.vocab_size and len(ids) > 1:
            pairs = [(ids[i], ids[i + 1]) for i in range(len(ids) - 1)]
            counts = Counter(pairs)
            best_pair, count = counts.most_common(1)[0]

            if count < 2:
                break

            new_id = len(self.id_to_token)

            self.id_to_token[new_id] = best_pair
            self.token_to_id[best_pair] = new_id
            self.merges.append(best_pair)

            new_ids = []
            i = 0

            while i < len(ids):
                if i < len(ids) - 1 and (ids[i], ids[i + 1]) == best_pair:
                    # i숫자가 들어온값들의 마지막 갯수보다작을 베스트페어와 비교한다
                    new_ids.append(new_id)
                    # 막만약 같다면 추가해라
                    i += 2
                else:
                    new_ids.append(ids[i])
                    i += 1

            ids = new_ids

        """
        TODO: 코퍼스에서 BPE merge rule과 vocabulary를 학습합니다.

        구현 힌트:
        - `corpus.encode("utf-8")`로 byte ID 시퀀스를 만듭니다.
        - 가장 자주 등장하는 이웃 token pair를 찾습니다.
        - 새 token ID를 만들고, 시퀀스의 해당 pair를 새 ID로 치환합니다.
        - `self.merges`, `self.id_to_token`, `self.token_to_id`를 갱신합니다.
        """
        raise NotImplementedError("BPETokenizer.train을 구현하세요.")

    def save(self, path: str | Path):
        """
        TODO: vocabulary와 merge rule을 JSON 파일로 저장합니다.

        bytes와 tuple은 JSON에 바로 저장할 수 없으므로 type 정보를 함께 저장하세요.
        """
        import json

        data = {
            "vocab_size": self.vocab_size,
            "merges": self.merges,
        }

        path = Path(path)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        raise NotImplementedError("BPETokenizer.save를 구현하세요.")

    def load(self, path: str | Path):
        """
        TODO: save()로 저장한 JSON 파일을 읽어 vocabulary와 merge rule을 복원합니다.
        """

        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))

        self.vocab_size = data["vocab_size"]
        self.id_to_token = {}
        self.token_to_id = {}
        self.merges = []

        self._init_special_tokens()

        for pair in data["merges"]:
            pair = tuple(pair)
            new_id = len(self.id_to_token)

            self.id_to_token[new_id] = pair
            self.token_to_id[pair] = new_id
            self.merges.append(pair)

        raise NotImplementedError("BPETokenizer.load를 구현하세요.")

    def encode(self, text: str, add_bos_eos: bool = False) -> list[int]:
        byte_values = text.encode("utf-8")
        ids = [BYTE_OFFSET + byte_value for byte_value in byte_values]

        for pair in self.merges:
            new_id = self.token_to_id[pair]
            new_ids = []
            i = 0

            while i < len(ids):
                if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
                    new_ids.append(new_id)
                    i += 2
                else:
                    new_ids.append(ids[i])
                    i += 1

            ids = new_ids

        if add_bos_eos:
            return [SPECIAL_IDS[BOS_TOKEN], *ids, SPECIAL_IDS[EOS_TOKEN]]
        return ids

    def decode(self, ids: list[int], skip_special: bool = True) -> str:
        byte_values = []

        def expand(token_id):
            if BYTE_OFFSET <= token_id < BYTE_OFFSET + NUM_BYTES:
                byte_values.append(token_id - BYTE_OFFSET)
            else:
                left, right = self.id_to_token[token_id]
                expand(left)
                expand(right)

        # 기본토큰일시에는 결과값에 넣고 아닐시에는 다시 분해를 진행하면 왼쪽부터 다시 재귀를 한다

        for token_id in ids:

            if skip_special and token_id in SPECIAL_IDS.values():
                continue

            expand(token_id)

        return bytes(byte_values).decode("utf-8")
        # 값을 utf-8 로 해석을 진행한다

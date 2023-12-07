import os

import openai

langs = {
    "ja": "日本語",
    "en": "English",
    "zh": "Chinese",
    "ko": "Korean",
}


class Translate:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(
        self,
        text: str,
        targets: list[str],
    ) -> str | None:
        target_lang_description = [langs[t] for t in targets]
        system_prompt = f"""
自然言語の翻訳をしてください.

翻訳元になる言語: 不明 (与えられる文から推測せよ)
翻訳先になる言語: {' / '.join(target_lang_description)}

ユーザーから文章が与えられます.
文章は
---
から
---
の間にあります.

あなたはこれを翻訳してください.
言語が複数ある場合はそれぞれの翻訳を順に行って, それらの結果を / で区切って並べてください.

例えば翻訳先: English / Chinese の場合, 入力に対するあなたの出力は次のとおりです

---
こんばんわ
---
Good evening / 晩上好
---

他の例も示します

---
おやすみなさい
---
Good night! / 晩安
---

翻訳先は一つかもしれません. English の場合,

---
こんばんわ
---
Good evening
---

---
おやすみなさい
---
Good night!
---

求められた言語にのみ適切に翻訳してください

マーカーとして --- を利用しているだけで, --- 自体は出力に含まれないことに注意してください.
もし含んでしまうとあなたはマイナスに評価されるので絶対に厳守してください.

ではこれから翻訳したい文章を次に与えます.
"""
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"""
---
{text}
---
""",
            },
        ]
        result = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
        )
        return result.choices[0].message.content

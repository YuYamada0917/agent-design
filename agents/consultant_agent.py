import anthropic
import config


class ConsultantAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def generate_prompt(self):
        print("Webデザインの要件を聞き取ります。以下の質問にお答えください。")

        purpose = input("1. Webサイトの目的は何ですか？: ")
        target_audience = input("2. ターゲット層はどのような人たちですか？: ")
        key_features = input("3. 含めたい主な機能やセクションは何ですか？: ")
        style_preference = input("4. 好みのデザインスタイル（例：モダン、ミニマリスト、カラフル）は？: ")
        color_scheme = input("5. 希望する色合いはありますか？: ")
        additional_info = input("6. その他、デザインに関して伝えたいことがあれば教えてください: ")
        language = input("7. webページの言語は何にしますか？: ")

        user_requirements = f"""
        Webサイトの要件:
        1. 目的: {purpose}
        2. ターゲット層: {target_audience}
        3. 主な機能/セクション: {key_features}
        4. デザインスタイル: {style_preference}
        5. 色合い: {color_scheme}
        6. 追加情報: {additional_info}
        7. 言語: {language}
        """

        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=3000,
            system="あなたは経験豊富なコンサルタントです。ユーザーの好みを聞き、webページの要件を明確にしてください。",
            messages=[
                {
                    "role": "user",
                    "content": f"以下の要件に基づいて、HTML、CSS、JavaScriptを含むWebデザイン生成のための最適なプロンプトを作成してください。生成されるHTMLファイルにはインラインでCSSとJavaScriptを含める必要があります。:\n\n{user_requirements}",
                }
            ],
        )

        return message.content

    def display_generated_prompt(self, prompt):
        print("\n生成されたプロンプト:")
        print(prompt)
        print("\nこのプロンプトを使用してWebデザインを生成します。")

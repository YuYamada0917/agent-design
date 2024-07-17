import anthropic
import config

class Agent2:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.modification_count = 0
        self.version_dir = None

    def set_version_dir(self, dir_path):
        self.version_dir = dir_path

    def generate_design(self, prompt):
        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=4000,
            messages=[
                {"role": "user", "content": f"""以下のプロンプトに基づいて、HTML、CSS、JavaScriptを含む完全なWebデザインを生成してください。
                HTMLファイルの中にインラインでCSSとJavaScriptを含めてください。
                必ず<!DOCTYPE html>から始まる完全なHTMLドキュメントを生成してください。
                HTMLドキュメント以外は出力しないでください。
                画像はプレースホルダーとして、以下のようなURLを使用してください：
                <img src="https://via.placeholder.com/500x300" alt="placeholder">

                プロンプト：
                {prompt}

                生成されたデザインは、ブラウザで直接開いて表示できる形式にしてください。"""
                }
            ]
        )
        return message.content

    def modify_design(self, design, feedback):
        if self.modification_count >= config.MAX_MODIFICATIONS:
            return design

        self.modification_count += 1
        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=4000,
            messages=[
                {"role": "user", "content": f"""以下のWebデザイン（HTML、CSS、JavaScript）を、次のフィードバックに基づいて修正してください。HTMLドキュメント以外は絶対に出力しないでください。

                重要な注意点:
                1. CSSとJavaScriptは必ずインラインのままにしてください。
                2. レスポンシブデザインを維持し、モバイル対応を忘れないでください。
                3. 機能性を損なわないように注意しながら、視覚的な改善を行ってください。
                4. フィードバックに基づいて修正を行いますが、元のデザインの良い部分は保持してください。
                5. 完全なHTMLドキュメントを提供してください。ブラウザで直接開いて表示できる形式にしてください。
                6. 大幅にデザインを変えるのを恐れないでください。改善のために必要な変更を行ってください。
                7.十分な量のコンテンツがあることを確認し、必要に応じて追加してください。
                8. 画像はプレースホルダーとして、以下のようなURLを使用してください
                   <img src="https://via.placeholder.com/500x300" alt="placeholder">

                現在のデザイン：
                {design}

                フィードバック：
                {feedback}

                修正後のデザインを完全なHTML形式（<!DOCTYPE html>から始まる）で提供してください。"""
                }
            ]
        )
        return message.content
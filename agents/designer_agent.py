import anthropic
import config
import re


class DesignerAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def evaluate_design(self, design):
        if isinstance(design, list) and len(design) > 0 and hasattr(design[0], "text"):
            design = design[0].text
        elif isinstance(design, str):
            pass
        else:
            raise ValueError("Unexpected design format")

        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1000,
            system="あなたは経験豊富なデザイナーです。webページのデザインを評価し、改善のためのフィードバックを提供してください",
            messages=[
                {
                    "role": "user",
                    "content": f"""以下のWebデザインを視覚的な観点から評価し、改善のためのフィードバックを提供してください。

                以下の5つの項目について、各10点満点で評価してください：
                1. 色彩のバランス：配色の調和、ブランドカラーの効果的な使用
                2. レイアウトの整合性：要素の配置、空白の効果的な利用、全体的な構造
                3. タイポグラフィの適切さ：フォントの選択、サイズ、行間、読みやすさ
                4. ビジュアル要素の質：画像、アイコン、グラフィックスの品質と適切さ
                5. ブランドアイデンティティとの一貫性：ロゴ、色彩、スタイルのブランドとの整合性

                各項目の評価点とその理由を述べてください。

                フィードバックは具体的で建設的なものにしてください。デザインの良い点も言及し、改善点については具体的な提案をしてください。

                デザイン：
                {design}

                回答は以下の形式で返してください：

                色彩のバランス: X/10
                レイアウトの整合性: X/10
                タイポグラフィの適切さ: X/10
                ビジュアル要素の質: X/10
                ブランドアイデンティティとの一貫性: X/10

                合計点数: XX/50

                フィードバック:
                (詳細なフィードバックをここに記述)
                """,
                }
            ],
        )

        content = (
            message.content[0].text
            if isinstance(message.content, list)
            else message.content
        )

        # 正規表現を使用して点数を抽出
        scores = {}
        score_pattern = (
            r"(色彩のバランス|レイアウトの整合性|タイポグラフィの適切さ|ビジュアル要素の質|ブランドアイデンティティとの一貫性):\s*(\d+)/10"
        )
        matches = re.findall(score_pattern, content)
        for category, score in matches:
            scores[category] = int(score)

        # 合計点数を抽出
        total_score_match = re.search(r"合計点数:\s*(\d+)/50", content)
        total_score = (
            int(total_score_match.group(1))
            if total_score_match
            else sum(scores.values())
        )

        # フィードバックを抽出
        feedback_match = re.search(r"フィードバック:\s*([\s\S]*)", content)
        feedback = (
            feedback_match.group(1).strip() if feedback_match else "フィードバックを抽出できませんでした。"
        )

        return total_score, feedback

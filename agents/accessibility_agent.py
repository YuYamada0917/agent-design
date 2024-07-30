import anthropic
import config
import re


class AccessibilityAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def evaluate_accessibility(self, design):
        if isinstance(design, list) and len(design) > 0 and hasattr(design[0], "text"):
            design = design[0].text
        elif isinstance(design, str):
            pass
        else:
            raise ValueError("Unexpected design format")

        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""以下のWebデザインのアクセシビリティを評価し、改善のためのフィードバックを提供してください。

                以下の5つの項目について、各10点満点で評価してください：
                1. スクリーンリーダー対応：適切な見出し構造、ARIAラベルの使用、フォーム要素のラベリング
                2. キーボードナビゲーション：全ての機能へのキーボードアクセス、フォーカスの視覚的表示
                3. コントラストと可読性：テキストと背景のコントラスト比、フォントサイズの適切さ
                4. 代替テキストの適切さ：画像、アイコン、ボタンなどの意味を伝える代替テキストの提供
                5. レスポンシブデザインの実装：異なる画面サイズでのレイアウト調整、タッチターゲットのサイズ

                各項目の評価点とその理由を述べてください。

                フィードバックは具体的で建設的なものにしてください。アクセシビリティの良い点も言及し、改善点については具体的な提案をしてください。

                デザイン：
                {design}

                回答は以下の形式で返してください：

                スクリーンリーダー対応: X/10
                キーボードナビゲーション: X/10
                コントラストと可読性: X/10
                代替テキストの適切さ: X/10
                レスポンシブデザインの実装: X/10

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
        score_pattern = r"(スクリーンリーダー対応|キーボードナビゲーション|コントラストと可読性|代替テキストの適切さ|レスポンシブデザインの実装):\s*(\d+)/10"
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

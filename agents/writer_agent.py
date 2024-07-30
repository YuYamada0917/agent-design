import anthropic
import config
import re


class WriterAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def evaluate_content(self, design):
        if isinstance(design, list) and len(design) > 0 and hasattr(design[0], "text"):
            design = design[0].text
        elif isinstance(design, str):
            pass
        else:
            raise ValueError("Unexpected design format")

        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1000,
            system="あなたは経験豊富なライターです。webページのコンテンツを評価し、改善のためのフィードバックを提供してください",
            messages=[
                {
                    "role": "user",
                    "content": f"""以下のWebデザインのコンテンツを評価し、改善のためのフィードバックを提供してください。

                以下の5つの項目について、各10点満点で評価してください：
                1. メッセージの明確さ：主要なメッセージや価値提案の明確さと簡潔さ
                2. コンテンツの関連性：ターゲットオーディエンスにとっての情報の適切さと有用性
                3. 文章の読みやすさ：文章構造、段落分け、専門用語の適切な使用
                4. 説得力：コンテンツの論理的な流れ、証拠や事例の効果的な使用
                5. コールトゥアクションの効果：明確で魅力的な行動喚起の提示

                各項目の評価点とその理由を述べてください。

                フィードバックは具体的で建設的なものにしてください。コンテンツの良い点も言及し、改善点については具体的な提案をしてください。

                デザイン：
                {design}

                回答は以下の形式で返してください：

                メッセージの明確さ: X/10
                コンテンツの関連性: X/10
                文章の読みやすさ: X/10
                説得力: X/10
                コールトゥアクションの効果: X/10

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
        score_pattern = r"(メッセージの明確さ|コンテンツの関連性|文章の読みやすさ|説得力|コールトゥアクションの効果):\s*(\d+)/10"
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

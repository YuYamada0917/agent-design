import anthropic
import config
import json
import re

class ReviewerAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def evaluate_design(self, design):
        if isinstance(design, list) and len(design) > 0 and hasattr(design[0], 'text'):
            design = design[0].text
        elif isinstance(design, str):
            pass
        else:
            raise ValueError("Unexpected design format")

        message = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"""以下のWebデザインを評価し、改善のためのフィードバックを提供してください。

                以下の5つの項目について、各10点満点で評価してください：
                1. 視覚的調和：色彩の使用とバランス、レイアウトの整合性、タイポグラフィの適切さ
                2. 創造性と独自性：独創的な要素の有無、記憶に残るデザイン要素
                3. 機能性とユーザビリティ：直感的な操作性、情報の階層構造の明確さ
                4. アクセシビリティ：異なるユーザー（視覚障害者など）への対応、様々なデバイスでの表示と操作性
                5. レスポンシブ性とモバイル対応：異なるデバイスやスクリーンサイズでの表示の適応性、モバイルでの使いやすさと読みやすさ
                
                各項目の評価点とその理由を述べてください。

                フィードバックは具体的で建設的なものにしてください。デザインの良い点も言及し、改善点については具体的な提案をしてください。

                デザイン：
                {design}

                回答は以下の形式で返してください：

                視覚的調和: X/10
                創造性と独自性: X/10
                機能性とユーザビリティ: X/10
                アクセシビリティ: X/10
                レスポンシブ性とモバイル対応: X/10

                合計点数: XX/50

                フィードバック:
                (詳細なフィードバックをここに記述)
                """
                }
            ]
        )
        
        content = message.content[0].text if isinstance(message.content, list) else message.content
        
        # 正規表現を使用して点数を抽出
        scores = {}
        score_pattern = r'(視覚的調和|創造性と独自性|機能性とユーザビリティ|アクセシビリティ|レスポンシブ性とモバイル対応):\s*(\d+)/10'
        matches = re.findall(score_pattern, content)
        for category, score in matches:
            scores[category] = int(score)
        
        # 合計点数を抽出
        total_score_match = re.search(r'合計点数:\s*(\d+)/50', content)
        total_score = int(total_score_match.group(1)) if total_score_match else sum(scores.values())
        
        # フィードバックを抽出
        feedback_match = re.search(r'フィードバック:\s*([\s\S]*)', content)
        feedback = feedback_match.group(1).strip() if feedback_match else "フィードバックを抽出できませんでした。"
        
        return total_score, feedback
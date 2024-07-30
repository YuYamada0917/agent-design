from agents.consultant_agent import ConsultantAgent
from agents.programmer_agent import ProgrammerAgent
from agents.designer_agent import DesignerAgent
from agents.writer_agent import WriterAgent
from agents.accessibility_agent import AccessibilityAgent
from utils.file_handler import create_version_directory, save_design_version
import config
import os

def extract_text_content(content):
    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], 'text'):
        return content[0].text
    elif isinstance(content, str):
        return content
    else:
        raise ValueError("Unexpected content format")

def save_html_file(content, version):
    directory = "generate_html"
    os.makedirs(directory, exist_ok=True)
    filename = f"index{version}.html"
    file_path = os.path.join(directory, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

def main():
    consultant = ConsultantAgent()
    programmer = ProgrammerAgent()
    designer = DesignerAgent()
    writer = WriterAgent()
    accessibility = AccessibilityAgent()

    version_dir = create_version_directory()
    programmer.set_version_dir(version_dir)

    prompt = consultant.generate_prompt()
    prompt = extract_text_content(prompt)
    consultant.display_generated_prompt(prompt)

    design = programmer.generate_design(prompt) 
    design = extract_text_content(design)
    version = 0

    design_urls = []

    for i in range(config.MAX_MODIFICATIONS + 1):
        version += 1
        file_path = save_html_file(design, version)
        url = f'file://{os.path.abspath(file_path)}'
        design_urls.append(url)
        
        print(f"\nバージョン {version} のデザインを生成しました。")
        print(f"ファイル: {file_path}")
        print(f"URL: {url}")
        
        try:
            design_score, design_feedback = designer.evaluate_design(design)
            content_score, content_feedback = writer.evaluate_content(design)
            accessibility_score, accessibility_feedback = accessibility.evaluate_accessibility(design)

            total_score = design_score + content_score + accessibility_score
            print(f"\n評価結果:")
            print(f"デザイン評価: {design_score}/50")
            print(f"コンテンツ評価: {content_score}/50")
            print(f"アクセシビリティ評価: {accessibility_score}/50")
            print(f"合計点数: {total_score}/150")

            print("\nデザインフィードバック:")
            print(design_feedback)
            print("\nコンテンツフィードバック:")
            print(content_feedback)
            print("\nアクセシビリティフィードバック:")
            print(accessibility_feedback)

            if total_score >= config.SCORE_THRESHOLD or i == config.MAX_MODIFICATIONS:
                print("\nデザイン生成プロセスが完了しました。")
                break
        except Exception as e:
            print(f"評価中にエラーが発生しました: {e}")
            print("デザイン生成プロセスを継続します。")
            total_score = 0
            design_feedback = content_feedback = accessibility_feedback = "評価に失敗しました。デザインの改善を続けます。"

        combined_feedback = f"""デザインフィードバック:
{design_feedback}

コンテンツフィードバック:
{content_feedback}

アクセシビリティフィードバック:
{accessibility_feedback}"""

        design = programmer.modify_design(design, combined_feedback)
        design = extract_text_content(design)

    print("\n各バージョンのデザインは以下のファイルで確認できます：")
    for i, url in enumerate(design_urls, 1):
        print(f"バージョン {i}: {url}")

if __name__ == "__main__":
    main()
from agents.agent1 import Agent1
from agents.agent2 import Agent2
from agents.agent3 import Agent3
from utils.file_handler import create_version_directory, save_design_version
import config

def extract_text_content(content):
    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], 'text'):
        return content[0].text
    elif isinstance(content, str):
        return content
    else:
        raise ValueError("Unexpected content format")

def main():
    agent1 = Agent1()
    agent2 = Agent2()
    agent3 = Agent3()

    version_dir = create_version_directory()
    agent2.set_version_dir(version_dir)

    prompt = agent1.generate_prompt()
    prompt = extract_text_content(prompt)
    agent1.display_generated_prompt(prompt)

    design = agent2.generate_design(prompt)
    design = extract_text_content(design)
    version = 0

    design_urls = []

    for i in range(config.MAX_MODIFICATIONS + 1):
        version += 1
        file_path = save_design_version(design, version, version_dir)
        url = f'file://{file_path}'
        design_urls.append(url)
        
        print(f"\nバージョン {version} のデザインを生成しました。")
        print(f"URL: {url}")
        
        try:
            total_score, feedback = agent3.evaluate_design(design)
            print(f"\nエージェント3の評価とフィードバック:")
            print(f"合計点数: {total_score}/50")
            print(feedback)

            if total_score >= 38 or i == config.MAX_MODIFICATIONS:
                print("\nデザイン生成プロセスが完了しました。")
                break
        except Exception as e:
            print(f"評価中にエラーが発生しました: {e}")
            print("デザイン生成プロセスを継続します。")
            total_score = 0
            feedback = "評価に失敗しました。デザインの改善を続けます。"

        design = agent2.modify_design(design, feedback)
        design = extract_text_content(design)

    print("各バージョンのデザインは以下のURLで確認できます：")
    for i, url in enumerate(design_urls, 1):
        print(f"バージョン {i}: {url}")

if __name__ == "__main__":
    main()
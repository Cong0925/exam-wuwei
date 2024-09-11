'''
# 交给gpt
以下是解决此问题的方法：

要遵循的步骤：
1. 数据集准备
您需要加载数据集的子集，其中包含多个问题和答案。HeadlineAdaptLLM/finance-tasks
2. 解析数据
您的任务是分解每个条目，提取每个问题及其相应的答案。
要使用的格式可能如下所示：
yaml
复制代码
Question 1: Yes
Question 2: No
...
3. 重新格式化的数据的结构
以结构化 JSON 格式存储每个提取的问题-答案对：
json
复制代码
{
  "id": "unique_id",
  "Question": "What is the question?",
  "Answer": "Yes/No"
}
您还可以根据需要添加相关标签或其他属性，以保持数据集的完整性。
4. 自动化
代码应处理数据集中的变体，例如问题和答案的不同格式。
不要手动编辑数据集 - 使用 Python 进行自动转换。
'''

# 示例代码
import json
import re
import time
import uuid

# 定义一个函数来解析每个条目并提取问答对
def parse_questions_answers(entry):
    # 使用正则表达式从条目中提取问题和答案
    pattern = r"(Question \d+):\s*(Yes|No)"
    matches = re.findall(pattern, entry)
    
    # 为每个问答对创建结构化的JSON格式
    qa_pairs = []
    for match in matches:
        question, answer = match
        qa_pairs.append({
            "id": str(uuid.uuid4()),  # 生成唯一标识符
            "Question": question,
            "Answer": answer
        })
    
    return qa_pairs

# 处理数据集的主要功能
def process_dataset(dataset):
    results = []
    for entry in dataset:
        qa_pairs = parse_questions_answers(entry['input'])
        results.extend(qa_pairs)
    
    return results

# 加载数据集（假设它在本地文件中或从URL获取）
# 数据集=load_your_datat_function（）

# 模拟数据集
dataset = [{"input": "Question 1: Yes Question 2: No"}, {"input": "Question 3: No Question 4: Yes"}]

# 追踪时间
start_time = time.time()

# 处理数据集
formatted_data = process_dataset(dataset)

# 以JSON格式保存结果
with open('formatted_data.json', 'w') as f:
    json.dump(formatted_data, f, indent=4)

# 结束时间
end_time = time.time()

# 计算统计数据
total_pairs = len(formatted_data)
processing_time = end_time - start_time

# 输出统计
print(f"Total question-answer pairs: {total_pairs}")
print(f"Time taken for processing: {processing_time} seconds")
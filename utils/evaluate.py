import re
from .math import is_equiv

# GSM8K
def extract_last_boxed_content(s):
    pattern = r"\\boxed{([^}]+)}"
    matches = re.findall(pattern, s)
    
    if matches:
        last_match = matches[-1]  
        cleaned_match = re.sub(r"[^-^0-9,.]", "", last_match)
        cleaned_match = cleaned_match.replace(",", "").strip()
        cleaned_match = cleaned_match.split(".0")[0]
        return cleaned_match
    else:
        return ''

def evaluate_gsm8k(result_list, data_list):
    correct_count = 0
    total_count = len(data_list)

    for i in range(total_count):
        result = extract_last_boxed_content(result_list[i])
        
        if str(data_list[i]['Answer']) in result:
            correct_count += 1

    accuracy = (correct_count / total_count) * 100
    return accuracy

# MATH
def last_boxed_only_string(answer: str):
    idx = answer.rfind("\\boxed")
    if idx < 0:
        idx = answer.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(answer):
        if answer[i] == "{":
            num_left_braces_open += 1
        if answer[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1
    
    if right_brace_idx == None:
        retval = None
    else:
        retval = answer[idx:right_brace_idx + 1]
    
    return retval

def get_answer(answer: str) -> str:
    boxed_content = last_boxed_only_string(answer)
    if boxed_content != None:
        boxed_content = boxed_content[7:]
        boxed_content = boxed_content[:-1]
        return boxed_content
    else:
        return ''


def evaluate_math(result_list, data):
    correct_count = 0
    total_count = len(data)

    for i in range(total_count):
        result = get_answer(result_list[i])
        # print(result)
        if is_equiv(result, data[i]['Answer']):
            correct_count += 1


    accuracy = (correct_count / total_count) * 100
    return accuracy

# tool
def normalize_string(s):
    s = s.replace(' ', '').replace('"', "'")
    s = s.replace('/', '')
    s = s.replace(',', '')
    s = s.lower()

    return s

def evaluate_tool_exact_output(result_list, data):
    correct_count = 0
    total_count = len(data)

    for i in range(total_count):
        result = normalize_string(result_list[i])
        expected = [normalize_string(ans) for ans in data[i]['Answer']]

        if all(ans in result for ans in expected):
            correct_count += 1

    accuracy = (correct_count / total_count) * 100
    return accuracy

def evaluate_tool_part_output(result_list, data):
    correct_count = 0
    total_count = len(data)

    for i in range(total_count):
        result = normalize_string(result_list[i])
        expected = [normalize_string(ans) for ans in data[i]['Answer']]

        if all(ans in result for ans in expected):
            correct_count += 1
        elif any(ans in result for ans in expected):
            correct_count += 0.5
        
        
    accuracy = (correct_count / total_count) * 100
    return accuracy
import os
from docx import Document # DOCX 파일 처리를 위해
from PyPDF2 import PdfReader # PDF 파일 처리를 위해

def extract_text_from_docx(filepath):
    """DOCX 파일에서 텍스트를 추출합니다."""
    doc = Document(filepath)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip(): # 비어있지 않은 단락만 추가
            full_text.append(para.text.strip())
    return full_text

def extract_text_from_pdf(filepath):
    """PDF 파일에서 텍스트를 추출합니다."""
    full_text = []
    try:
        reader = PdfReader(filepath)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                # PDF 텍스트는 줄바꿈 등이 불규칙할 수 있으므로, 줄 단위로 나누어 정리합니다.
                for line in text.splitlines():
                    stripped_line = line.strip()
                    if stripped_line:
                        full_text.append(stripped_line)
    except Exception as e:
        print(f"  PDF 파일 '{filepath}'에서 텍스트를 추출하는 중 오류가 발생했습니다: {e}")
        print("  이 파일은 처리되지 않을 수 있습니다. ㅠㅠ")
    return full_text

def consolidate_and_deduplicate_all_formats(input_folder, output_file_name):
    """다양한 형식(DOCX, PDF)의 파일에서 텍스트를 추출하고 중복을 제거하여 하나의 파일로 저장합니다."""
    
    unique_lines_or_paragraphs = set()
    
    print(f"'{input_folder}' 폴더에서 파일을 읽는 중입니다...\n")

    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        extracted_content = []

        if filename.endswith(".docx"):
            print(f"  DOCX 파일 '{filename}'에서 텍스트 추출 중...")
            extracted_content = extract_text_from_docx(filepath)
        elif filename.endswith(".pdf"):
            print(f"  PDF 파일 '{filename}'에서 텍스트 추출 중...")
            extracted_content = extract_text_from_pdf(filepath)
        else:
            # 다른 형식의 파일은 건너뜁니다.
            continue
            
        for item in extracted_content:
            stripped_item = item.strip()
            if stripped_item:
                unique_lines_or_paragraphs.add(stripped_item)
                
    print(f"\n총 {len(unique_lines_or_paragraphs)}개의 중복 없는 대화 내용을 찾았습니다.")

    # 새로운 파일에 중복 제거된 내용 저장
    try:
        with open(output_file_name, 'w', encoding='utf-8') as outfile:
            for line in sorted(list(unique_lines_or_paragraphs)): # 보기 좋게 정렬해서 저장
                outfile.write(line + '\n')
        print(f"'{output_file_name}' 파일에 성공적으로 저장했습니다! 정말 뿌듯하네요 ㅎㅎ")
    except Exception as e:
        print(f"파일 '{output_file_name}'을 저장하는 중 오류가 발생했습니다: {e}")

# --- 사용 예시 ---
# 1. 'my_conversations'라는 폴더 안에 모든 DOCX와 PDF 파일을 넣어주세요.
# 2. 아래 'input_directory' 변수 값을 해당 폴더 경로로 변경하세요.
input_directory = 'my_conversations' 
output_document = 'consolidated_dialogues.txt'

# 폴더가 존재하지 않으면 생성
if not os.path.exists(input_directory):
    print(f"'{input_directory}' 폴더가 존재하지 않아 생성합니다.")
    os.makedirs(input_directory)
    print(f"DOCX 파일 56개와 PDF 파일 4개를 '{input_directory}' 폴더에 넣어주세요.")
else:
    consolidate_and_deduplicate_all_formats(input_directory, output_document)

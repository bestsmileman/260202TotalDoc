import os
from docx import Document  # DOCX 파일 처리를 위해
from PyPDF2 import PdfReader  # PDF 파일 처리를 위해

def extract_text_from_docx(filepath):
    """DOCX 파일에서 텍스트를 추출합니다."""
    try:
        doc = Document(filepath)
        full_text = []
        for para in doc.paragraphs:
            stripped_text = para.text.strip()
            if stripped_text: # 비어있지 않은 단락만 추가
                full_text.append(stripped_text)
        return full_text
    except Exception as e:
        print(f"  [오류] DOCX 파일 '{filepath}'에서 텍스트를 추출하는 중 문제가 발생했습니다: {e}")
        print("  이 파일은 처리되지 않을 수 있습니다. ㅠㅠ")
        return []

def extract_text_from_pdf(filepath):
    """PDF 파일에서 텍스트를 추출합니다."""
    full_text = []
    try:
        reader = PdfReader(filepath)
        # 모든 페이지를 순회하며 텍스트 추출
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
        print(f"  [오류] PDF 파일 '{filepath}'에서 텍스트를 추출하는 중 문제가 발생했습니다: {e}")
        print("  이 파일은 처리되지 않을 수 있습니다. ㅠㅠ")
    return full_text

def consolidate_and_deduplicate_all_formats(input_folder, output_file_name):
    """다양한 형식(DOCX, PDF)의 파일에서 텍스트를 추출하고 중복을 제거하여 하나의 파일로 저장합니다."""
    
    unique_lines_or_paragraphs = set() # 중복을 제거하기 위해 set 사용
    
    print(f"\n[알림] '{input_folder}' 폴더에서 파일을 읽는 중입니다...\n")

    file_count = 0
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        extracted_content = []

        if filename.endswith(".docx"):
            print(f"  DOCX 파일 '{filename}' 처리 중...")
            extracted_content = extract_text_from_docx(filepath)
            file_count += 1
        elif filename.endswith(".pdf"):
            print(f"  PDF 파일 '{filename}' 처리 중...")
            extracted_content = extract_text_from_pdf(filepath)
            file_count += 1
        # 다른 형식의 파일은 자동으로 건너뜁니다.
            
        for item in extracted_content:
            stripped_item = item.strip()
            if stripped_item:
                unique_lines_or_paragraphs.add(stripped_item)
                
    print(f"\n[완료] 총 {file_count}개의 파일을 처리하여 {len(unique_lines_or_paragraphs)}개의 중복 없는 대화 내용을 찾았습니다.")

    # 새로운 파일에 중복 제거된 내용 저장
    try:
        with open(output_file_name, 'w', encoding='utf-8') as outfile:
            # 내용을 가나다순으로 정렬해서 저장하면 나중에 보기 더 편할 거예요!
            for line in sorted(list(unique_lines_or_paragraphs)): 
                outfile.write(line + '\n')
        print(f"[성공] '{output_file_name}' 파일에 성공적으로 저장했습니다! 정말 뿌듯하네요 ㅎㅎ")
    except Exception as e:
        print(f"[오류] 파일 '{output_file_name}'을 저장하는 중 문제가 발생했습니다: {e}")

# --- 아주님 사용을 위한 실행 부분 ---
# 스크립트가 실행되는 현재 폴더를 기준으로 'my_conversations' 폴더에서 파일을 찾고,
# 'consolidated_dialogues.txt' 파일을 현재 폴더에 생성합니다.
input_directory = 'my_conversations' 
output_document = 'consolidated_dialogues.txt' 

# 입력 폴더가 존재하는지 확인하고, 없으면 사용자에게 안내합니다.
if not os.path.exists(input_directory):
    print(f"\n[안내] '{os.getcwd()}\\{input_directory}' 폴더가 존재하지 않습니다.")
    print(f"      DOCX 파일 56개와 PDF 파일 4개를 넣어둘 '{input_directory}' 폴더를 생성한 뒤,")
    print(f"      모든 대화 파일들을 그 폴더 안에 넣어주세요.")
    print("\n[다음 단계] 폴더 준비 후 스크립트를 다시 실행해주세요.")
else:
    print(f"\n--- '{os.getcwd()}\\{input_directory}' 폴더에 있는 파일들을 처리합니다. ---")
    consolidate_and_deduplicate_all_formats(input_directory, output_document)

# parser.py
import re

class TRECParser:
    def parse_documents(self, filename):
        documents = []
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            # Find all <DOC> ... </DOC>
            docs = re.findall(r'<DOC>(.*?)</DOC>', data, re.DOTALL)
            for doc in docs:
                # Extract DOCNO
                docno_match = re.search(r'<DOCNO>(.*?)</DOCNO>', doc)
                docno = docno_match.group(1).strip() if docno_match else 'UNKNOWN'
                # Extract TEXT
                text_matches = re.findall(r'<TEXT>(.*?)</TEXT>', doc, re.DOTALL)
                text_content = ' '.join(text_matches)
                documents.append({'docno': docno, 'content': text_content})
        return documents

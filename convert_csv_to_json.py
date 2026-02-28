import csv
import json

def main():
    data_map = {}
    
    # Token fields that contain aligned data
    token_fields = {
        'traditional', 'POS', 'gloss', 'chr realization', 
        'Mandarin', 'Cantonese', 'KoreanUm', 
        'JapaneseKun', 'JapaneseOn', 'stratum', 'syntactic note'
    }
    
    # Metadata fields that contain a single value
    metadata_fields = {
        'sentence', '2010次序', '2010頁碼', '2016頁碼', 
        'speaker', 'zh2', 'en2', 'annotations', 'scan'
    }

    with open('source.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
                
            entry_id = row[0].strip()
            field_type = row[1].strip()
            
            if not entry_id:
                 continue

            if not field_type:
                continue

            if entry_id not in data_map:
                data_map[entry_id] = {
                    "id": entry_id,
                    "metadata": {},
                    "tokens": []
                }
            
            entry = data_map[entry_id]
            
            if field_type in metadata_fields:
                if len(row) > 2:
                    entry["metadata"][field_type] = row[2]
            
            elif field_type in token_fields:
                tokens_data = row[2:]
                for i, val in enumerate(tokens_data):
                    val = val.strip()
                    if not val:
                        continue
                    while len(entry["tokens"]) <= i:
                        entry["tokens"].append({})
                    entry["tokens"][i][field_type] = val

    final_output = []
    # Sort keys to ensure order 1, 2, 3...
    def sort_key(k):
        if k.isdigit():
            return (0, int(k))
        return (1, k)

    sorted_ids = sorted(data_map.keys(), key=sort_key)
    
    for eid in sorted_ids:
        entry = data_map[eid]
        # entry["tokens"] might have gaps or be too long?
        # Actually with "while len <= i", we fill gaps with empty dicts.
        # But we might have trailing empty dicts if we extended too far? 
        # No, because we only extend if `val` is not empty.
        # So the length is determined by the max index of non-empty data.
        # However, intermediate gaps (e.g. empty column in middle) will be empty dicts.
        # This is correct behavior for alignment.
        
        final_output.append(entry)

    with open('brushtalk.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

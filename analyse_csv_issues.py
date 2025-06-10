import csv
import re

def find_csv_issues(filepath):
    """
    Find lines with unescaped quote characters in CSV file
    """
    issues = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            # Check for unescaped quotes (quotes not at field boundaries)
            # Look for quotes that aren't properly escaped or at field start/end
            if '"' in line:
                # Count quotes - should be even number for properly escaped CSV
                quote_count = line.count('"')
                
                # Look for patterns that indicate unescaped quotes
                # Pattern: text"text (quote in middle of field)
                unescaped_pattern = r'[^,"]"[^,"]'
                if re.search(unescaped_pattern, line):
                    issues.append({
                        'line_number': line_num,
                        'line_content': line.strip(),
                        'quote_count': quote_count,
                        'issue_type': 'unescaped_quote'
                    })
                # Check for odd number of quotes (incomplete escaping)
                elif quote_count % 2 != 0:
                    issues.append({
                        'line_number': line_num,
                        'line_content': line.strip(),
                        'quote_count': quote_count,
                        'issue_type': 'odd_quotes'
                    })
    
    return issues

def analyze_specific_lines_detailed(filepath, line_numbers):
    """
    Analyze specific line numbers with detailed character inspection
    """
    target_lines = set(line_numbers)
    found_lines = {}
    
    with open(filepath, 'rb') as file:  # Open in binary mode
        for line_num, line_bytes in enumerate(file, 1):
            if line_num in target_lines:
                # Get both string and hex representation
                try:
                    line_str = line_bytes.decode('utf-8').strip()
                except UnicodeDecodeError:
                    line_str = line_bytes.decode('utf-8', errors='replace').strip()
                
                # Find all quote-like characters
                quote_chars = []
                for i, char in enumerate(line_str):
                    if char in ['"', "'", '"', '"', '`', '´', ''', ''']:
                        quote_chars.append(f"Position {i}: '{char}' (Unicode: U+{ord(char):04X})")
                
                found_lines[line_num] = {
                    'content': line_str,
                    'raw_bytes': line_bytes.hex(),
                    'quote_chars': quote_chars,
                    'length': len(line_str)
                }
    
    return found_lines

# Main execution
if __name__ == "__main__":
    filepath = "data/raw/olist_customers_dataset.csv"
    
    print("🔍 Detailed CSV analysis for quote issues...")
    print(f"File: {filepath}\n")
    
    # Check the specific problematic lines from the error
    error_lines = [122575, 122576, 122577, 122578, 122579]
    detailed_analysis = analyze_specific_lines_detailed(filepath, error_lines)
    
    print("📍 Detailed analysis of problematic lines:")
    for line_num in sorted(detailed_analysis.keys()):
        data = detailed_analysis[line_num]
        print(f"\n--- Line {line_num} ---")
        print(f"Content: {data['content']}")
        print(f"Length: {data['length']} characters")
        if data['quote_chars']:
            print(f"Quote-like characters found:")
            for quote_info in data['quote_chars']:
                print(f"  {quote_info}")
        else:
            print("No obvious quote characters found")
        
        # Show first 100 bytes in hex for inspection
        hex_preview = data['raw_bytes'][:200]  # First 100 bytes
        print(f"Raw bytes (first 100): {hex_preview}")
    
    print("\n" + "="*60)
    
    # Also try to read with different CSV settings
    print("\n🔧 Testing CSV parsing:")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i + 1 in error_lines:
                    print(f"Line {i+1} parsed as: {len(row)} fields")
                    if len(row) > 5:  # Expected: 5 fields for geolocation
                        print(f"  Too many fields! Expected 5, got {len(row)}")
                        print(f"  Fields: {row}")
                if i > max(error_lines):
                    break
    except Exception as e:
        print(f"CSV parsing error: {e}")
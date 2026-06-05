import os
from src.chunking import ChunkingStrategyComparator

def main():
    docs = [
        "data/bocongan/100152.txt",
        "data/bocongan/118633.txt"
    ]
    
    comparator = ChunkingStrategyComparator()
    
    for doc_path in docs:
        print(f"=== Document: {doc_path} ===")
        with open(doc_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        print(f"Total length: {len(text)}")
        result = comparator.compare(text, chunk_size=500)
        
        for strategy, stats in result.items():
            print(f"Strategy: {strategy}")
            print(f"  Chunk Count: {stats['count']}")
            print(f"  Avg Length: {stats['avg_length']:.2f}")
        print()

if __name__ == "__main__":
    main()

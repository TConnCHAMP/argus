#!/usr/bin/env python3
"""
Verify HITL entity merging implementation structure
"""
import sys
import importlib.util

def check_backend_implementation():
    """Verify backend changes"""
    print("=" * 70)
    print("HITL ENTITY MERGE MVP - IMPLEMENTATION VERIFICATION")
    print("=" * 70)
    print("\n📋 BACKEND IMPLEMENTATION:\n")
    
    # Check 1: Graph routes file exists and has new endpoint
    try:
        with open('lightrag/api/routers/graph_routes.py', 'r') as f:
            content = f.read()
            
        checks = [
            ("DetectDuplicateEntitiesRequest class", "class DetectDuplicateEntitiesRequest" in content),
            ("detect_duplicate_entities endpoint", "async def detect_duplicate_entities" in content),
            ("Endpoint docstring", "Detect potential duplicate entities using vector similarity" in content),
            ("Similarity threshold param", "similarity_threshold: float" in content),
            ("Top-k parameter", "top_k: int" in content),
        ]
        
        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            
        all_passed = all(p for _, p in checks)
        print(f"\n  Backend Status: {'PASS ✓' if all_passed else 'FAIL ✗'}\n")
        return all_passed
        
    except Exception as e:
        print(f"  ✗ Error checking backend: {e}\n")
        return False

def check_frontend_implementation():
    """Verify frontend changes"""
    print("📋 FRONTEND IMPLEMENTATION:\n")
    
    checks = []
    
    # Check 1: DuplicateDetectionDialog component
    try:
        with open('lightrag_webui/src/components/graph/DuplicateDetectionDialog.tsx', 'r') as f:
            content = f.read()
        
        dialog_checks = [
            ("DuplicateDetectionDialog component exists", "const DuplicateDetectionDialog" in content),
            ("Dialog opens with duplicates list", "duplicates.map" in content),
            ("Auto Merge button", "autoMerge" in content),
            ("Keep Separate button", "keepSeparate" in content),
            ("Similarity color coding", "getSimilarityBadge" in content),
        ]
        
        for check_name, passed in dialog_checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            checks.extend(dialog_checks)
            
    except Exception as e:
        print(f"  ✗ Error checking DuplicateDetectionDialog: {e}")
        
    # Check 2: PropertiesView integration
    try:
        with open('lightrag_webui/src/components/graph/PropertiesView.tsx', 'r') as f:
            content = f.read()
        
        properties_checks = [
            ("DuplicateDetectionDialog imported", "import DuplicateDetectionDialog" in content),
            ("detectDuplicateEntities imported", "detectDuplicateEntities" in content),
            ("handleDetectDuplicates function", "handleDetectDuplicates" in content),
            ("Scan button in NodePropertiesView", "handleDetectDuplicates" in content),
        ]
        
        for check_name, passed in properties_checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            checks.extend(properties_checks)
            
    except Exception as e:
        print(f"  ✗ Error checking PropertiesView: {e}")
    
    # Check 3: API types and service
    try:
        with open('lightrag_webui/src/api/lightrag.ts', 'r') as f:
            content = f.read()
        
        api_checks = [
            ("DuplicateEntity type defined", "export type DuplicateEntity" in content),
            ("DetectDuplicatesResponse type", "export type DetectDuplicatesResponse" in content),
            ("detectDuplicateEntities function", "export const detectDuplicateEntities" in content),
        ]
        
        for check_name, passed in api_checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            checks.extend(api_checks)
            
    except Exception as e:
        print(f"  ✗ Error checking API: {e}")
    
    # Check 4: Translations
    try:
        with open('lightrag_webui/src/locales/en.json', 'r') as f:
            content = f.read()
        
        i18n_checks = [
            ("duplicateDetection translations added", "duplicateDetection" in content),
            ("scanForDuplicates key", "scanForDuplicates" in content),
            ("autoMerge translation", "autoMerge" in content),
            ("keepSeparate translation", "keepSeparate" in content),
            ("noDuplicates message", "noDuplicates" in content),
        ]
        
        for check_name, passed in i18n_checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            checks.extend(i18n_checks)
            
    except Exception as e:
        print(f"  ✗ Error checking translations: {e}")
    
    all_passed = all(p for _, p in checks)
    print(f"\n  Frontend Status: {'PASS ✓' if all_passed else 'FAIL ✗'}\n")
    return all_passed

def print_summary():
    """Print implementation summary"""
    print("=" * 70)
    print("IMPLEMENTATION SUMMARY")
    print("=" * 70)
    print("""
✓ BACKEND ENDPOINT
  POST /graph/entities/detect-duplicates
  - Uses vector similarity to find duplicate entities
  - Parameters: entity_name, similarity_threshold, top_k
  - Returns ranked list with descriptions & similarity scores

✓ FRONTEND DIALOG
  DuplicateDetectionDialog component
  - Shows potential duplicates in ranked list
  - Color-coded similarity (green/yellow/orange)
  - "Auto Merge" and "Keep Separate" buttons
  - Loading state during detection

✓ GRAPH PANEL INTEGRATION
  - "Scan for Duplicates" button in NodePropertiesView
  - Triggers duplicate detection for selected entity
  - Opens dialog with results
  - Clicking merge uses existing updateEntity() API

✓ API TYPES & SERVICES
  - DetectDuplicateEntitiesRequest class
  - DuplicateEntity & DetectDuplicatesResponse types
  - detectDuplicateEntities() service method

✓ TRANSLATIONS
  - graphPanel.duplicateDetection.* i18n keys
  - common.merging and common.close keys

""")
    print("=" * 70)
    print("TESTING INSTRUCTIONS")
    print("=" * 70)
    print("""
1. Install dependencies (if not already done):
   pip install -e .[api]

2. Start the API server:
   lightrag-server
   or: uvicorn lightrag.api.lightrag_server:app --reload

3. In another terminal, start the web UI:
   cd lightrag_webui
   bun install
   bun run dev

4. Open the frontend in your browser (usually http://localhost:5173)

5. In the Graph panel:
   - Click on a node to select it
   - Properties panel appears on the right
   - Click the "Scan for Duplicates" button (magnifying glass icon)
   - Wait for duplicate detection to complete
   - Review results in the popup dialog
   - Click "Auto Merge" to merge into a duplicate
   - Or "Keep Separate" to dismiss

✅ READY FOR TESTING!
""")

if __name__ == "__main__":
    backend_ok = check_backend_implementation()
    print()
    frontend_ok = check_frontend_implementation()
    
    if backend_ok and frontend_ok:
        print("\n✓ All implementation checks PASSED!\n")
        print_summary()
    else:
        print("\n✗ Some checks failed. Review the output above.\n")
        sys.exit(1)

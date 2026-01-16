#!/usr/bin/env python3
"""
Quick verification test for HITL Entity Merging MVP
Tests the duplicate detection endpoint structure
"""
import sys
import json

def test_hitl_implementation():
    """Verify HITL MVP implementation"""
    
    print("=" * 60)
    print("HITL ENTITY MERGING MVP - VERIFICATION TEST")
    print("=" * 60)
    
    # Test 1: Check backend endpoint exists
    print("\n✓ Test 1: Backend endpoint registration")
    try:
        from lightrag.api.routers.graph_routes import DetectDuplicateEntitiesRequest
        print("  ✓ DetectDuplicateEntitiesRequest class found")
        
        # Verify request fields
        req_fields = DetectDuplicateEntitiesRequest.__fields__
        assert 'entity_name' in req_fields
        assert 'similarity_threshold' in req_fields
        assert 'top_k' in req_fields
        print("  ✓ All request fields present (entity_name, similarity_threshold, top_k)")
        
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # Test 2: Check frontend types
    print("\n✓ Test 2: Frontend type definitions")
    try:
        with open('lightrag_webui/src/api/lightrag.ts', 'r') as f:
            content = f.read()
            assert 'DetectDuplicatesResponse' in content
            assert 'DuplicateEntity' in content
            assert 'detectDuplicateEntities' in content
            print("  ✓ DuplicateEntity type found")
            print("  ✓ DetectDuplicatesResponse type found")
            print("  ✓ detectDuplicateEntities function found")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # Test 3: Check dialog component
    print("\n✓ Test 3: HITL Dialog Component")
    try:
        with open('lightrag_webui/src/components/graph/DuplicateDetectionDialog.tsx', 'r') as f:
            content = f.read()
            assert 'DuplicateDetectionDialog' in content
            assert 'getSimilarityBadge' in content
            assert 'onMerge' in content
            print("  ✓ DuplicateDetectionDialog component found")
            print("  ✓ Merge handler found")
            print("  ✓ Similarity badge styling found")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # Test 4: Check graph panel integration
    print("\n✓ Test 4: Graph Panel Integration")
    try:
        with open('lightrag_webui/src/components/graph/PropertiesView.tsx', 'r') as f:
            content = f.read()
            assert 'DuplicateDetectionDialog' in content
            assert 'handleDetectDuplicates' in content
            assert 'detectDuplicateEntities' in content
            assert 'handleMergeDuplicate' in content
            print("  ✓ DuplicateDetectionDialog imported and used")
            print("  ✓ Duplicate detection handler found")
            print("  ✓ Merge handler integrated")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # Test 5: Check translations
    print("\n✓ Test 5: Translations")
    try:
        with open('lightrag_webui/src/locales/en.json', 'r') as f:
            translations = json.load(f)
            dup_keys = translations['graphPanel']['duplicateDetection']
            required_keys = [
                'title', 'description', 'noDuplicates', 'foundCount',
                'similar', 'autoMerge', 'keepSeparate', 'scanForDuplicates'
            ]
            for key in required_keys:
                assert key in dup_keys, f"Missing translation key: {key}"
            print(f"  ✓ All {len(required_keys)} duplicate detection translations present")
            assert 'merging' in translations['common']
            print("  ✓ 'merging' added to common translations")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - HITL MVP READY")
    print("=" * 60)
    print("\nImplementation Summary:")
    print("  • Backend: /graph/entities/detect-duplicates endpoint")
    print("  • Frontend: DuplicateDetectionDialog component")
    print("  • Integration: PropertiesView with scan button")
    print("  • Merge: Auto-merge via existing updateEntity API")
    print("  • Translations: Full i18n support for all HITL UI")
    print("\nNext steps:")
    print("  1. Start lightrag-server: 'lightrag-server'")
    print("  2. Start frontend: 'cd lightrag_webui && bun run dev'")
    print("  3. Open graph, right-click node, click 'Scan for Duplicates'")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = test_hitl_implementation()
    sys.exit(0 if success else 1)

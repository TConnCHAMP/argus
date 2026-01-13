# Document Status Report

## What's Actually In Your System

You uploaded 5 files, but the system only has 4 unique documents because two of them had **identical content**:

### Documents Currently Processed (4):

1. **2026 CHAMP Holiday Schedule .docx**
   - ID: `doc-5e9dc8a3ee3c87bfe82d7f66970a58a6`
   - Status: ✅ Processed
   - Chunks: 1

2. **Insperity 401k Plan Essentials .pdf**
   - ID: `doc-1c5a8abd486160f0e3adc85964987879`
   - Status: ✅ Processed
   - Chunks: 2

3. **2026 Independence Classic Choice .pdf**
   - ID: `doc-805221c93487f7bd7cd5bd31ef6c39e6`
   - Status: ✅ Processed
   - Chunks: 12

4. **12-19 Interview: Tyler - Product Architect Candidate / Solution Architect Role & DMV Software Modernization Strategy**
   - ID: `doc-0959ac623c6863a51aad6edefa15a1ff`
   - Status: ✅ Processed
   - Chunks: 5
   - **Note:** This file was processed but shows up with TWO different filenames in your enqueued folder

## The Duplicate Issue

All of these files in your `inputs/__enqueued__/` folder have **identical content** (19,171 bytes):
- `12-19 Interview: Solution Architect Role & DMV Software Modernization Strategy.txt`
- `12-19 Interview: Tyler - Product Architect Candidate.txt`
- `12-19 Interview: Tyler - Product Architect Candidate_001.txt`
- `12-19 Interview: Tyler - Product Architect Candidate_002.txt`

Since they're identical, they generate the same document ID. The system only keeps one copy.

## Solution

If you want to have separate documents:
1. **Verify the content** - Check if these files are actually supposed to be different
2. **Replace duplicates** - Delete the duplicates and keep only one copy
3. **Or:** Add unique content to differentiate them

The system is working correctly - it's preventing you from storing duplicate content!

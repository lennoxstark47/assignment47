# Project Development Instructions

## Project Timeline & Git Workflow

This project follows a **weekly milestone approach** as outlined in the UG-Form.docx. Each week has a specific task that should be completed and committed separately to show realistic, progressive development.

### Important Principles

1. **One milestone per week/commit** - Don't complete multiple weeks at once
2. **Follow the exact timeline** - Each commit should match the planned milestone
3. **Show progressive development** - Git history should reflect step-by-step progress
4. **No future work** - Don't implement features from later milestones early

## Project Timeline

| Week Starting | Milestone | Branch/Commit Name |
|---------------|-----------|-------------------|
| **10/11/25** | Set up development environment; experiment with Web Audio API/Librosa | `claude/setup-audio-dev-environment-...` |
| **17/11/25** | Implement audio file upload and basic waveform display | `claude/audio-upload-waveform-...` |
| **24/11/25** | Develop feature extraction module (MFCC or chroma features) | `claude/feature-extraction-...` |
| **1/12/25** | Implement similarity calculation algorithm | `claude/similarity-calculation-...` |
| **8/12/25** | Build comparison visualization interface | `claude/comparison-visualization-...` |
| **15/12/25** | Compile test dataset; begin initial accuracy testing | `claude/test-dataset-accuracy-...` |
| **19/1/26** | Refine algorithms based on test results | `claude/algorithm-refinement-...` |
| **2/2/26** | Design user testing questionnaire | `claude/user-testing-questionnaire-...` |
| **9/2/26** | Conduct user testing (2 weeks) | `claude/user-testing-...` |
| **23/2/26** | Analyze user feedback; implement improvements | `claude/feedback-improvements-...` |
| **2/3/26** | Prepare project showcase materials | `claude/showcase-materials-...` |
| **9/3/26** | Begin final report writing | `claude/final-report-...` |
| **23/3/26** | Project Showcase | - |
| **30/3/26** | Finalize report and code documentation | `claude/finalize-documentation-...` |
| **30/4/26** | Submit final report (6,000 words) | - |

## Workflow for Each Milestone

### When Starting a New Milestone

1. **Read the milestone description** from the timeline above
2. **Create/checkout the appropriate branch** with the naming pattern shown
3. **Implement ONLY that week's feature** - nothing more, nothing less
4. **Test the specific feature** for that milestone
5. **Commit with a descriptive message** referencing the week and milestone
6. **Push to the branch**

### Example: Week of 10/11/25

**Milestone:** "Set up development environment; experiment with Web Audio API/Librosa"

**What to do:**
- ✅ Set up Python virtual environment
- ✅ Install Librosa and dependencies
- ✅ Create basic Librosa experiment script
- ✅ Create basic Web Audio API HTML experiment
- ✅ Document findings in simple markdown
- ❌ Don't build full Flask API (that's future work)
- ❌ Don't build complete React frontend (that's future work)
- ❌ Don't implement upload endpoints (that's week 17/11/25)

**Files for this milestone:**
```
backend/
├── requirements.txt
└── experiments/
    ├── librosa_experiment.py
    ├── test_audio.wav
    ├── librosa_features.png
    └── librosa_results.json

web_audio_experiment.html
TECH_STACK_EVALUATION.md
.gitignore
```

### Example: Week of 17/11/25 (NEXT MILESTONE)

**Milestone:** "Implement audio file upload and basic waveform display"

**What to do:**
- ✅ Create Flask app with upload endpoint
- ✅ Build basic HTML/React form for file upload
- ✅ Implement waveform visualization
- ✅ Test with sample audio files
- ❌ Don't extract MFCCs yet (that's week 24/11/25)
- ❌ Don't implement similarity calculation (that's week 1/12/25)

## Git Commands for Each Milestone

```bash
# When starting a new milestone
git checkout -b claude/[milestone-name]-[session-id]

# After completing the milestone work
git add .
git commit -m "[Week DD/MM/YY] [Milestone description]

[Detailed description of what was implemented]

Files:
- [list key files added/modified]
"

# Push to remote
git push -u origin claude/[milestone-name]-[session-id]
```

## What Each Milestone Should Include

### Week 10/11/25 ✅ COMPLETED
- Backend environment setup
- Librosa experiment demonstrating features
- Web Audio API basic experiment
- Comparison notes
- Simple documentation

### Week 17/11/25 ✅ COMPLETED
- Flask app with upload route
- Basic frontend with file input
- Waveform display functionality
- Testing with MP3/WAV files

### Week 24/11/25 (NEXT)
- Feature extraction module (MFCC/Chroma)
- Integration with upload system
- Save/retrieve extracted features
- Performance testing

### Week 1/12/25
- Similarity calculation algorithms (DTW, cosine)
- API endpoint for comparison
- Testing with similar/different tracks

### Week 8/12/25
- Visualization of similarity results
- Highlighted sections display
- Percentage score display
- User-friendly results page

## Common Mistakes to Avoid

❌ **Don't do this:**
- Implementing multiple weeks at once
- Building complete features too early
- Creating production-ready code in early milestones
- Over-engineering solutions

✅ **Do this:**
- Follow the timeline strictly
- Implement minimal viable features for each week
- Keep it simple and progressive
- Show realistic development pace

## Checking Your Work

Before committing, ask:
1. ✅ Does this match ONLY the current week's milestone?
2. ✅ Have I avoided implementing future features?
3. ✅ Is this a reasonable amount of work for one week?
4. ✅ Does the commit message reference the correct date?
5. ✅ Am I on the correct branch with session ID in the name?

## Current Status

**Completed Milestones:**
- ✅ Week 10/11/25: Development environment setup + experiments
- ✅ Week 17/11/25: Audio file upload and basic waveform display

**Next Milestone:**
- ⏭️ Week 24/11/25: Develop feature extraction module (MFCC or chroma features)

**Current Branch:**
- `claude/week-17-11-25-milestone-01Wi2sstenjWAxzAnYDKy9Sy`

## Notes for AI Assistant

When asked to work on this project:

1. **Always ask which milestone** we're working on
2. **Check INSTRUCTIONS.md** for the timeline
3. **Implement only that milestone's features** - nothing more
4. **Use appropriate branch naming** with session ID
5. **Create realistic commit messages** with the week date
6. **Don't rush ahead** - respect the timeline
7. **Keep code simple** - early milestones should be experimental/basic

## Testing Each Milestone

Each milestone should be testable:

- **10/11/25:** Run experiment scripts, see results
- **17/11/25:** Upload a file, see waveform
- **24/11/25:** Extract features, verify MFCC output
- **1/12/25:** Compare two files, get similarity score
- **8/12/25:** View comparison results visually

## Project Goals

**Final Deliverables (by May 2026):**
- Working web application for music similarity detection
- 80%+ accuracy on plagiarism detection
- Processing time < 30 seconds
- User testing results (15-20 participants)
- 6,000-word technical report
- Code documentation

**Current Phase:** Week 2 of 32 weeks - Implementation phase ✅

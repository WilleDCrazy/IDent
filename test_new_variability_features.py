#!/usr/bin/env python3
"""
Test script for the NEW sentence-level variability features.
"""

from ident import StyleAnalyzer

# Sample text with more variability (human-like)
human_varied_text = """
I love coding! It's amazing. Sometimes I write long, complex sentences that contain multiple clauses, detailed explanations, and various punctuation marks to express nuanced ideas.
Then I switch it up. Short ones. Quick thoughts! You know?

Why do we even do this, though? It's a question worth exploring in depth, considering all the various factors that contribute to our decision-making processes. But then again... maybe not. Life's too short for overthinking every little detail, right?

The cat sat on the mat. Meanwhile, the dog was running around the garden with unbridled enthusiasm, chasing butterflies and barking at imaginary threats. Everything was peaceful (mostly).
"""

# AI-like text with uniformity
ai_uniform_text = """
The research demonstrates significant findings. Moreover, the data analysis reveals important patterns. Furthermore, the methodology employed was particularly robust. Additionally, the results were remarkably consistent across all test groups.

The study utilized advanced techniques. The researchers implemented comprehensive protocols. The findings indicated substantial improvements. The conclusions drawn were notably significant.

However, the implications extend beyond this scope. Nevertheless, the results remain highly relevant. Therefore, the recommendations are critically important. Consequently, further research is essential.
"""

def main():
    print("Testing NEW Sentence-Level Variability Features")
    print("=" * 70)

    analyzer = StyleAnalyzer(min_words=20)

    # New variability features to test
    new_features = [
        'avg_punct_types_per_sentence',
        'punct_diversity_variance',
        'avg_word_length_var_per_sentence',
        'sentence_rhythm_variability',
        'consecutive_sentence_similarity',
        'punctuation_variance_per_sentence',
        'consecutive_lexical_overlap',
        'sentence_complexity_variance'
    ]

    # Analyze human-like text
    print("\n1. Human-like Text (VARIED, NATURAL):")
    print("-" * 70)
    human_profile = analyzer.analyze(human_varied_text, name="Human Varied")

    for feature in new_features:
        if feature in human_profile.features:
            value = human_profile.features[feature]
            print(f"  {feature:.<50} {value:.4f}")

    # Analyze AI-like text
    print("\n2. AI-like Text (UNIFORM, CONSISTENT):")
    print("-" * 70)
    ai_profile = analyzer.analyze(ai_uniform_text, name="AI Uniform")

    for feature in new_features:
        if feature in ai_profile.features:
            value = ai_profile.features[feature]
            print(f"  {feature:.<50} {value:.4f}")

    # Compare
    print("\n3. Comparison (Human vs AI):")
    print("-" * 70)
    print("Higher values = MORE variability (more human-like)")
    print("Lower values = LESS variability (more AI-like)")
    print()

    for feature in new_features:
        if feature in human_profile.features and feature in ai_profile.features:
            human_val = human_profile.features[feature]
            ai_val = ai_profile.features[feature]
            diff = human_val - ai_val
            indicator = "✓ Human more varied" if diff > 0.01 else ("✓ AI more varied" if diff < -0.01 else "≈ Similar")
            print(f"  {feature:.<40} H: {human_val:6.3f}  AI: {ai_val:6.3f}  {indicator}")

    print("\n" + "=" * 70)
    print("Test completed successfully!")
    print(f"Total features extracted: {len(human_profile.features)}")
    print("\n✨ KEY INSIGHT:")
    print("Human text should show HIGHER variability in:")
    print("  - Punctuation diversity per sentence")
    print("  - Word length variance within sentences")
    print("  - Sentence rhythm changes")
    print("  - Sentence complexity variance")
    print("\nAI text tends to be more uniform and consistent! ✨")

if __name__ == "__main__":
    main()

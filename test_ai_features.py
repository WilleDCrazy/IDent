#!/usr/bin/env python3
"""
Test script for the new AI-detection features.
"""

from ident import StyleAnalyzer

# Sample text that might have AI-like characteristics
ai_like_text = """
However, the implications of this research are significant. Moreover, the data suggests
that furthermore, we must consider the various factors. Nevertheless, the results are
remarkably consistent with our hypothesis. Specifically, the findings indicate that
particularly in cases where the methodology was applied correctly.

The analysis was conducted carefully—using multiple approaches—to ensure accuracy.
Therefore, the conclusions drawn are fundamentally sound. Additionally, the data
effectively demonstrates the key principles. Consequently, we can substantially
confirm the original theory. Notably, the patterns observed are distinctly different
from previous studies.

The methodology is described in detail. The results were analyzed thoroughly.
The conclusions are presented clearly. The implications are discussed extensively.
"""

# More natural human-like text
human_like_text = """
Jag tyckte verkligen om filmen igår. Det var spännande från början till slut, även om
vissa scener kändes lite långdragna. Min kompis sa att hon trodde slutet var
förutsägbart, men jag håller inte med. Skådespelarna gjorde ett fantastiskt jobb!

Vi gick och åt efteråt på den där nya restaurangen vid torget. Maten var okej, inte
mer än så. Jag beställde pasta och den smakade ganska bra, men portionen var lite
liten för priset. Nästa gång kanske vi provar något annat ställe istället.

Vädret var underbart hela dagen. Solen sken och det var varmt men inte för varmt.
Perfekt för en promenad hemåt. Nu ska jag läsa lite innan jag somnar. God natt!
"""

def main():
    print("Testing AI-Detection Features")
    print("=" * 60)

    analyzer = StyleAnalyzer(min_words=20)

    # Analyze AI-like text
    print("\n1. AI-like Text Analysis:")
    print("-" * 60)
    ai_profile = analyzer.analyze(ai_like_text, name="AI-like Text")

    ai_features = [
        'em_dashes_per_sentence',
        'em_dash_frequency',
        'lines_per_sentence',
        'transition_word_frequency',
        'transition_word_ratio',
        'sentence_starter_diversity',
        'sentence_starter_repetition',
        'passive_voice_frequency',
        'adverb_frequency',
        'adverb_ratio',
        'sentence_length_uniformity',
        'complex_punctuation_frequency',
        'parenthetical_per_sentence'
    ]

    for feature in ai_features:
        if feature in ai_profile.features:
            value = ai_profile.features[feature]
            print(f"  {feature:.<45} {value:.4f}")

    # Analyze human-like text
    print("\n2. Human-like Text Analysis:")
    print("-" * 60)
    human_profile = analyzer.analyze(human_like_text, name="Human-like Text")

    for feature in ai_features:
        if feature in human_profile.features:
            value = human_profile.features[feature]
            print(f"  {feature:.<45} {value:.4f}")

    # Compare
    print("\n3. Comparison (AI-like vs Human-like):")
    print("-" * 60)
    for feature in ai_features:
        if feature in ai_profile.features and feature in human_profile.features:
            ai_val = ai_profile.features[feature]
            human_val = human_profile.features[feature]
            diff = ai_val - human_val
            print(f"  {feature:.<35} AI: {ai_val:6.3f}  Human: {human_val:6.3f}  Diff: {diff:+.3f}")

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print(f"Total features extracted: {len(ai_profile.features)}")

if __name__ == "__main__":
    main()

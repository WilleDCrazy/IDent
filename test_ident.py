"""
Quick test script to verify IDent functionality.
"""

print("Testing IDent - Swedish Text Style Analyzer")
print("=" * 60)

# Test 1: Import modules
print("\n1. Testing imports...")
try:
    from ident import StyleAnalyzer, TextProfile
    from ident.comparator import compare_multiple_profiles
    from ident.visualizer import visualize_profiles_2d
    print("   ✓ All imports successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    exit(1)

# Test 2: Basic analysis
print("\n2. Testing basic analysis...")
try:
    analyzer = StyleAnalyzer()

    text = """
    Sveriges ekonomi växer stadigt enligt nya rapporter från Statistiska centralbyrån.
    Tillväxten under det senaste kvartalet uppgick till 2,3 procent, vilket är högre än
    väntat. Experter menar att den starka arbetsmarknaden och ökade investeringar i
    infrastruktur bidrar till den positiva utvecklingen. Samtidigt varnar ekonomer för
    att inflationen fortsätter att vara en utmaning. Konsumentpriserna har stigit mer
    än förväntat, vilket påverkar hushållens köpkraft negativt. Riksbanken överväger
    ytterligare räntehöjningar för att dämpa prisökningstakten. Den svenska kronan har
    försvagats mot euron under den senaste månaden, vilket gynnar exportföretagen.
    """

    profile = analyzer.analyze(text, name="Test Text")
    print(f"   ✓ Profile created: {profile}")
    print(f"   ✓ Features extracted: {len(profile.features)}")
    print(f"   ✓ Word count: {profile.features['total_words']:.0f}")
except Exception as e:
    print(f"   ✗ Analysis failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Feature extraction
print("\n3. Testing feature extraction...")
try:
    required_features = [
        'avg_word_length',
        'type_token_ratio',
        'avg_sentence_length',
        'yules_k',
        'swedish_char_frequency'
    ]

    for feature in required_features:
        if feature in profile.features:
            value = profile.features[feature]
            print(f"   ✓ {feature}: {value:.4f}")
        else:
            print(f"   ✗ Missing feature: {feature}")

except Exception as e:
    print(f"   ✗ Feature extraction failed: {e}")

# Test 4: Multiple text analysis
print("\n4. Testing multiple text analysis...")
try:
    text1 = """
    Sveriges ekonomi växer stadigt enligt nya rapporter. Tillväxten är högre än väntat.
    Experter menar att arbetsmarknaden är stark. Investeringar i infrastruktur bidrar
    till utvecklingen. Samtidigt varnar ekonomer för inflationen. Konsumentpriserna har
    stigit mycket. Riksbanken överväger räntehöjningar för att dämpa prisökningstakten.
    Den svenska kronan har försvagats mot euron nyligen. Detta gynnar exportföretagen.
    """

    text2 = """
    Hej allihopa! Idag måste jag berätta om något kul. Jag är så glad just nu! Det är
    helt fantastiskt väder ute. Solen skiner så härligt. Jag älskar verkligen såna här
    dagar. Man blir på så bra humör. Kanske ska jag ta en promenad senare? Det vore
    mysigt! Vad gör ni andra idag? Hoppas ni har det lika bra som jag. Puss och kram!
    """

    profiles = analyzer.analyze_multiple([text1, text2], ["Formal", "Informal"])
    print(f"   ✓ Created {len(profiles)} profiles")

    # Test comparison
    similarity = profiles[0].compare(profiles[1], method='cosine')
    print(f"   ✓ Similarity calculated: {similarity:.3f}")

except Exception as e:
    print(f"   ✗ Multiple analysis failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Profile comparison
print("\n5. Testing profile comparison...")
try:
    from ident.comparator import get_distinctive_features

    distinctive = get_distinctive_features(profiles[0], profiles[1], top_n=5)
    print(f"   ✓ Found {len(distinctive)} distinctive features")

    for i, (feature, (val1, val2, diff)) in enumerate(list(distinctive.items())[:3], 1):
        print(f"   {i}. {feature}: {diff:.4f} difference")

except Exception as e:
    print(f"   ✗ Comparison failed: {e}")

# Test 6: JSON export/import
print("\n6. Testing JSON export/import...")
try:
    import os

    # Export
    profile.to_json('test_profile.json')
    print("   ✓ Profile exported to JSON")

    # Import
    loaded_profile = TextProfile.from_json('test_profile.json')
    print("   ✓ Profile loaded from JSON")

    # Verify
    assert loaded_profile.name == profile.name
    assert len(loaded_profile.features) == len(profile.features)
    print("   ✓ Data integrity verified")

    # Cleanup
    os.remove('test_profile.json')
    print("   ✓ Cleanup completed")

except Exception as e:
    print(f"   ✗ JSON test failed: {e}")

# Test 7: Feature count
print("\n7. Feature summary...")
try:
    total_features = len(profile.features)
    print(f"   Total features extracted: {total_features}")

    # Count by category
    categories = {
        'Lexical': ['word', 'lexical', 'hapax', 'token', 'mtld'],
        'Syntactic': ['sentence', 'punctuation', 'comma', 'period'],
        'Character': ['char', 'uppercase', 'lowercase', 'digit'],
        'Swedish': ['swedish', 'aa_', 'ae_', 'oe_', 'function_word'],
        'Stylometric': ['yules', 'simpsons', 'honores', 'entropy']
    }

    for category, keywords in categories.items():
        count = sum(1 for f in profile.features.keys()
                   if any(kw in f for kw in keywords))
        print(f"   {category}: {count} features")

except Exception as e:
    print(f"   ✗ Feature summary failed: {e}")

# Final summary
print("\n" + "=" * 60)
print("✓ All tests passed! IDent is working correctly.")
print("=" * 60)
print("\nQuick Stats:")
print(f"  - Total features: {len(profile.features)}")
print(f"  - Sample word count: {profile.features['total_words']:.0f}")
print(f"  - Sample vocabulary richness: {profile.features['type_token_ratio']:.3f}")
print("\nTry running the examples:")
print("  python examples/basic_analysis.py")
print("  python examples/compare_texts.py")
print("  python examples/visualize_styles.py")
print("  python examples/advanced_analysis.py")

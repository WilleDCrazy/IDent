"""
Basic text analysis example using IDent.

This example shows how to:
1. Analyze a single Swedish text
2. Extract and display features
3. Print a formatted report
"""

from ident import StyleAnalyzer

# Sample Swedish text (news article style)
text1 = """
Sveriges ekonomi växer stadigt enligt nya rapporter från Statistiska centralbyrån.
Tillväxten under det senaste kvartalet uppgick till 2,3 procent, vilket är högre än
väntat. Experter menar att den starka arbetsmarknaden och ökade investeringar i
infrastruktur bidrar till den positiva utvecklingen.

Samtidigt varnar ekonomer för att inflationen fortsätter att vara en utmaning.
Konsumentpriserna har stigit mer än förväntat, vilket påverkar hushållens köpkraft
negativt. Riksbanken överväger ytterligare räntehöjningar för att dämpa prisökningstakten.

Den svenska kronan har försvagats mot euron under den senaste månaden, vilket
gynnar exportföretagen men gör importerade varor dyrare. Många företag inom
tillverkningsindustrin rapporterar starka orderingångar från utlandet.

Arbetslösheten ligger kvar på en låg nivå, men det råder brist på kvalificerad
arbetskraft inom flera sektorer. Särskilt teknologibranschen och byggsektorn
efterfrågar fler utbildade medarbetare. Regeringen har aviserat satsningar på
vidareutbildning och omskolning för att möta arbetsmarknadens behov.

Framtidsutsikterna för svensk ekonomi är försiktigt optimistiska. Internationella
handelskonflikter och geopolitiska spänningar utgör dock risker som kan påverka
tillväxten negativt. Många analytiker betonar vikten av fortsatta strukturreformer
och investeringar i innovation för att säkerställa långsiktig konkurrenskraft.
"""

# Initialize analyzer
print("Initializing StyleAnalyzer...")
analyzer = StyleAnalyzer()

# Analyze text
print("\nAnalyzing text...")
profile = analyzer.analyze(text1, name="Swedish News Article")

# Print full report
profile.print_report()

# Access specific features
print("\n" + "="*60)
print("Key Features:")
print("="*60)
print(f"Total words: {profile.features['total_words']:.0f}")
print(f"Total sentences: {profile.features['total_sentences']:.0f}")
print(f"Average word length: {profile.features['avg_word_length']:.2f} characters")
print(f"Average sentence length: {profile.features['avg_sentence_length']:.2f} words")
print(f"Type-Token Ratio: {profile.features['type_token_ratio']:.3f}")
print(f"Lexical Diversity (MTLD): {profile.features['mtld']:.2f}")
print(f"Swedish character frequency: {profile.features['swedish_char_frequency']:.4f}")
print(f"Yule's K: {profile.features['yules_k']:.2f}")
print("="*60)

# Save profile to JSON
profile.to_json('news_article_profile.json')
print("\nProfile saved to: news_article_profile.json")

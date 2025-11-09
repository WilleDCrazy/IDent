"""
Advanced analysis example using IDent.

This example shows how to:
1. Perform batch analysis
2. Create comparison matrices
3. Find distinctive features
4. Cluster similar texts
5. Export results
"""

from ident import StyleAnalyzer
from ident.comparator import (
    compare_multiple_profiles,
    create_feature_comparison_table,
    cluster_profiles,
    calculate_profile_centroid,
    calculate_profile_deviation
)
import pandas as pd

# Sample Swedish texts from different genres
texts = {
    "News 1": """
    Sveriges ekonomi växer stadigt enligt nya rapporter från Statistiska centralbyrån.
    Tillväxten under det senaste kvartalet uppgick till 2,3 procent, vilket är högre
    än väntat. Experter menar att den starka arbetsmarknaden och ökade investeringar
    i infrastruktur bidrar till den positiva utvecklingen. Samtidigt varnar ekonomer
    för att inflationen fortsätter att vara en utmaning. Konsumentpriserna har stigit
    mer än förväntat, vilket påverkar hushållens köpkraft negativt. Riksbanken överväger
    ytterligare räntehöjningar för att dämpa prisökningstakten och stabilisera ekonomin.
    """,

    "News 2": """
    Regeringen presenterade idag sitt nya budgetförslag för kommande år. Satsningar på
    utbildning och sjukvård står i centrum för de planerade investeringarna. Ministern
    betonade vikten av att säkerställa välstånd och välfärd för alla medborgare. Opposition
    kritiserar förslaget och menar att skatterna ökar för mycket. Debatt väntas i riksdagen
    nästa vecka. Analys från ekonomiska experter visar på både fördelar och nackdelar med
    förslaget. Fackförbund välkomnar satsningarna på arbetsmarknadsåtgärder och kompetensutveckling.
    """,

    "Blog 1": """
    Hej alla goa människor! Idag blev det lite spontanshopping i stan. Hittade faktiskt
    några riktigt snygga kläder på rea! Älskar när det händer. Man blir så glad av att
    hitta fynd. Köpte en supersöt tröja och ett par jeans. Passade perfekt! Sen tog jag
    och min kompis en fika på vårt favorithak. Vi satt där i typ två timmar och snackade
    om allt möjligt. Det var så mysigt! På kvällen blev det Netflix och chips hemma i
    soffan. Perfekt avslutning på en härlig dag! Nu ska jag sova gott. Puss och kram!
    """,

    "Blog 2": """
    Måste bara säga att jag är så trött på allt dåligt väder! Regnar ju hela tiden nu för
    tiden. Blir så less. Man vill ju bara att solen ska komma fram lite. Behöver verkligen
    lite D-vitamin! Hur mår ni andra? Klarar ni av höstmörkret? Jag brukar tända massa
    ljus hemma för att göra det mysigare. Hjälper faktiskt lite. Har också börjat träna
    mer för att få energi. Det funkar bra! Tips till er andra som känner er trötta: rör
    på er och ät nyttig mat. Gör underverk! Ha en bra dag allihopa! Kram kram.
    """,

    "Academic": """
    Denna studie undersöker språklig variation i digitala kommunikationskontexter med
    fokus på stilistiska och pragmatiska dimensioner. Metodologin baseras på korpuslingvistiska
    analysverktyg kombinerade med diskursanalytiska ramverk. Resultaten indikerar signifikanta
    skillnader mellan formella och informella kommunikationssituationer. Syntaktisk komplexitet
    varierar systematiskt korrelerat med kontextuella faktorer. Lexikala val uppvisar
    tydliga mönster relaterade till textgenre och målgrupp. Analyserna belyser hur digitala
    medier påverkar språklig produktion och reception fundamentalt. Implikationerna för
    språkvetenskaplig teori och praktisk tillämpning diskuteras ingående i avhandlingens
    slutkapitel.
    """,
}

# Initialize analyzer
print("="*70)
print("Advanced Swedish Text Style Analysis")
print("="*70)
print("\nInitializing analyzer...")
analyzer = StyleAnalyzer()

# Analyze all texts
print("\nAnalyzing texts...")
profiles = []
for name, text in texts.items():
    profile = analyzer.analyze(text, name=name)
    profiles.append(profile)
    print(f"  ✓ {name} ({profile.features['total_words']:.0f} words)")

print(f"\nTotal profiles created: {len(profiles)}")

# 1. Similarity Matrix
print("\n" + "="*70)
print("1. SIMILARITY MATRIX (Cosine Similarity)")
print("="*70)
similarity_df = compare_multiple_profiles(profiles, method='cosine')
print(similarity_df.to_string())

# 2. Feature Comparison Table
print("\n" + "="*70)
print("2. TOP VARIABLE FEATURES ACROSS TEXTS")
print("="*70)
feature_table = create_feature_comparison_table(profiles, top_n=12)
print(feature_table.to_string())

# 3. Clustering
print("\n" + "="*70)
print("3. AUTOMATIC CLUSTERING (K-Means, k=3)")
print("="*70)
try:
    clusters = cluster_profiles(profiles, n_clusters=3, method='kmeans')
    for cluster_id, cluster_profiles in clusters.items():
        print(f"\nCluster {cluster_id + 1}:")
        for profile in cluster_profiles:
            print(f"  - {profile.name}")
except Exception as e:
    print(f"Clustering failed: {e}")

# 4. Centroid Analysis
print("\n" + "="*70)
print("4. CENTROID ANALYSIS")
print("="*70)
centroid = calculate_profile_centroid(profiles)
print("Calculated centroid (average profile) from all texts\n")

print("Deviation from centroid:")
for profile in profiles:
    deviation = calculate_profile_deviation(profile, centroid)
    print(f"  {profile.name:.<30} {deviation:.4f}")

# 5. Genre-specific Analysis
print("\n" + "="*70)
print("5. GENRE-SPECIFIC FEATURE ANALYSIS")
print("="*70)

# Separate by genre
news_profiles = [p for p in profiles if "News" in p.name]
blog_profiles = [p for p in profiles if "Blog" in p.name]

if news_profiles:
    news_centroid = calculate_profile_centroid(news_profiles)
    print("\nNews articles - Key features:")
    sorted_features = sorted(news_centroid.items(), key=lambda x: abs(x[1]), reverse=True)[:8]
    for feature, value in sorted_features:
        print(f"  {feature.replace('_', ' ').title():.<45} {value:.4f}")

if blog_profiles:
    blog_centroid = calculate_profile_centroid(blog_profiles)
    print("\nBlog posts - Key features:")
    sorted_features = sorted(blog_centroid.items(), key=lambda x: abs(x[1]), reverse=True)[:8]
    for feature, value in sorted_features:
        print(f"  {feature.replace('_', ' ').title():.<45} {value:.4f}")

# 6. Export Results
print("\n" + "="*70)
print("6. EXPORTING RESULTS")
print("="*70)

# Export similarity matrix
similarity_df.to_csv('similarity_matrix.csv')
print("✓ Similarity matrix saved to: similarity_matrix.csv")

# Export feature table
feature_table.to_csv('feature_comparison.csv')
print("✓ Feature comparison saved to: feature_comparison.csv")

# Export individual profiles
for profile in profiles:
    filename = f"profile_{profile.name.replace(' ', '_').lower()}.json"
    profile.to_json(filename)
    print(f"✓ Profile saved to: {filename}")

print("\n" + "="*70)
print("Analysis completed!")
print("="*70)
